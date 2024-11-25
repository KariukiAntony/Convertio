from flask import Flask
import json, os
from werkzeug.exceptions import HTTPException
from auth.models import db, migrate, User
from auth.config import config_dict
from auth.auth import auth


def create_app(config=None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    print(os.environ.get("DATABASE_URL"))
    db.init_app(app)
    migrate.init_app(app)

    #register blueprints 
    app.register_blueprint(auth)
    
    @app.shell_context_processor
    def context_processor():
        return {"db": db, "User": User}

    # before any request
    @app.before_request
    def create_db():
        with app.app_context():
            db.create_all()

    # handle errors
    @app.errorhandler(HTTPException)
    def handle_exceptions(error):
        response = error.get_response()
        response.data = json.dumps(
            {
                "status code": error.code,
                "name": error.name,
                "description": error.description,
            }
        )
        response.content_type = "application/json"
        return response

    return app
