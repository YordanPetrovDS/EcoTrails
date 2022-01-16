from flask_restful import Resource
from managers.auth import auth
from managers.ecotrail import EcotrailManager
from managers.user import UserManager
from models import RoleType
from utils.decorators import permission_required


class CreateAdmin(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    def put(self, id_):
        UserManager.create_admin(id_)
        return 201


class CreateModerator(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    def put(self, id_):
        UserManager.create_moderator(id_)
        return 201


class DemoteModerator(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    def put(self, id_):
        UserManager.demote_moderator(id_)
        return 201


class DeleteUserEcotrailPost(Resource):
    @auth.login_required
    @permission_required(RoleType.administrator)
    def delete(self, id_):
        EcotrailManager.delete_user_ecotrail(id_)
        return {"message": "Success"}, 204
