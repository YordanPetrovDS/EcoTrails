from flask import request
from flask_cors import cross_origin
from flask_restful import Resource
from managers.user import UserManager
from schemas.request.user import RequestLoginUserSchema, RequestRegisterUserSchema
from utils.decorators import validate_schema


class RegisterUser(Resource):
    @validate_schema(RequestRegisterUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.register_user(data)
        return {"token": token}, 201


class LoginUser(Resource):
    @validate_schema(RequestLoginUserSchema)
    @cross_origin()
    def post(self):
        data = request.get_json()
        token = UserManager.login_user(data)
        return {"token": token, "role": "user"}, 200


class LoginModerator(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login_moderator(data)
        return {"token": token, "role": "moderator"}, 200


class LoginAdministrator(Resource):
    @validate_schema(RequestLoginUserSchema)
    def post(self):
        data = request.get_json()
        token = UserManager.login_admin(data)
        return {"token": token, "role": "administator"}, 200
