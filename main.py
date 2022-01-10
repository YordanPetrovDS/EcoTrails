from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from psycopg2.errorcodes import UNIQUE_VIOLATION
from werkzeug.exceptions import BadRequest, InternalServerError

from config import DevelopmentConfig
from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

migrate = Migrate(app, db)
CORS(app)
api = Api(app)

[api.add_resource(*r) for r in routes]


# @app.before_first_request
# def create_tables():
#     db.init_app(app)
#     db.create_all()


@app.after_request
def close_request(response):
    try:
        db.session.commit()
    except Exception as ex:
        if ex.orig.pgcode == UNIQUE_VIOLATION:
            raise BadRequest("Please login")
        else:
            InternalServerError("Server is an unavailable. Please try again later")
    return response


if __name__ == "__main__":
    app.run()
