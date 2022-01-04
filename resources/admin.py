from flask_restful import Resource
from flask import request

from managers.auth import auth
from managers.user import UserManager
from models import RoleType
from schemas.request.user import RequestCreateAdminSchema, RequestCreateModeratorSchema
from utils.decorators import validate_schema, permission_required


class CreateAdmin(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    @validate_schema(RequestCreateAdminSchema)
    def post(self):
        data = request.get_json()
        UserManager.create_admin(data)
        return 201


class CreateModerator(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    @validate_schema(RequestCreateModeratorSchema)
    def post(self):
        data = request.get_json()
        UserManager.create_moderator(data)
        return 201
