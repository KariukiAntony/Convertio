import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass

path = find_dotenv()
load_dotenv(find_dotenv())
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@dataclass
class BaseConfig(object):
    SECRET_KEY: str = os.urandom(20)
    DEBUG: bool = False
    TESTING: bool = False

    @staticmethod
    def init_app(app):
        pass


@dataclass
class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATION: bool = False
    SQLALCHEMY_ECHO: bool = False


@dataclass
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATION: bool = False
    SQLALCHEMY_ECHO: bool = False


@dataclass
class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = "sqlite://"
    TESTING: bool = True


config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}