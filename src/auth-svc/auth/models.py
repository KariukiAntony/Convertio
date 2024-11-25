from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import exc
from auth.utils import hash_pwd, verify_password

db = SQLAlchemy()
migrate = Migrate()


class Helper(object):
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        try:
            db.session.commit()
            return True
        except exc.IntegrityError as e:
            db.session.rollback()
            return False


class User(Helper, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer(), primary_key=True, index=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(500), unique=True, nullable=False)
    _password = db.Column(db.String(500), nullable=False)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = hash_pwd(password)

    @classmethod
    def get_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        else:
            return False
    @classmethod 
    def login_user(cls, data: dict):
        user = cls.get_user_by_email(data.get("email"))
        if user:
            return verify_password(data.get("password"), user.password)
        return False

    def to_json(self):
        return {
            "username": self.username,
            "email": self.email,
        }
