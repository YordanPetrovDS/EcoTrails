from decouple import config
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes


class DevelopmentConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
        f"@localhost:{config('DB_PORT')}/{config('DB_NAME')}"
    )


# class TestingConfig:
#     DEBUG = True
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = (
#         f"postgresql://{config('DB_USER')}:{config('DB_PASSWORD')}"
#         f"@localhost:{config('DB_PORT')}/{config('TEST_DB_NAME')}"
#     )


class TestingConfig:
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:Newlife7@localhost:5432/test_db"


def create_app(config="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config)
    migrate = Migrate(app, db)
    CORS(app)
    api = Api(app)
    [api.add_resource(*r) for r in routes]
    return app
