from flask import Blueprint, jsonify, request
from auth.models import User
from auth.utils import generate_token, decode_token

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print(data)
    status, message = validate_data(data, "register")
    if status == False:
        return make_response("failed", message, 400)

    new_user = User(**data)
    new_user.save_to_db()
    return make_response("success", "user created successfully", 201)


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    print(data)
    status, message = validate_data(data, "login")
    if status == False:
        return make_response("failed", message, 401)
    if User.login_user(data):
        payload = {"email": data.get("email")}
        token = generate_token(payload, True, 1)
        return jsonify({"status": "success", "access_token": token}), 200
    else:
        return make_response("failed", "Invalid email or password", 401)
    
@auth.route("/validate")
def validate_jwt():
    try:
        auth = request.headers["Authorization"]
        if auth:
            token = auth.split(" ")[1]
            decoded_jwt = decode_token(token)
            if decoded_jwt:
                return decoded_jwt, 200
            else:
                return 'Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'} 
        else:
            return 'Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}

    except Exception as error:
        return 'Unauthorized', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'}


def validate_data(data, endpoint="register"):
    required = {}
    if endpoint == "register":
        required = {"username", "email", "password"}
    else:
        required = {"email", "password"}
    data_fields = set(data.keys())
    if required == data_fields:
        return True, None
    else:
        missing = required - data_fields
        extra = data_fields - required
        if missing:
            return False, f"Validation failed: Missing fields - {missing}"
        if extra:
            return False, f"Validation failed: Unexpected fields - {missing}"


def make_response(status, message, status_code):
    return jsonify({"status": status, "message": message}), status_code
