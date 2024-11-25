import requests, os 
from dotenv import load_dotenv

load_dotenv()
AUTH_SVC_ADDRESS = os.environ.get("AUTH_SVC_ADRESS")
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def register(request):
    response = requests.post(f"{AUTH_SVC_ADDRESS}/register", json=request.get_json(), headers=headers)
    return response

def login(request):
    response = requests.post(f"{AUTH_SVC_ADDRESS}/login", json=request.get_json(), headers=headers)
    return response

def validate(request):
    token = request.headers.get("Authorization", None)
    if token:
        headers["Authorization"] = token
        response = requests.get(f"{AUTH_SVC_ADDRESS}/validate", headers=headers)
        if response.status_code == 200:
            return response.text, None
        else:
            return None, response.text
    else:
        return None, "Unauthorized"