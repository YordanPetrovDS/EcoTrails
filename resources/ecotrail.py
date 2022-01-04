from flask import request
from flask_restful import Resource
from managers.auth import auth
from managers.ecotrail import EcotrailManager
from models.enums import RoleType
from schemas.request.ecotrail import RequestEcotrailSchema
from schemas.response.ecotrail import ResponseEcotrailSchema
from utils.decorators import permission_required, validate_schema


class CreateEcotrailList(Resource):
    @auth.login_required
    def get(self):
        user = auth.current_user()
        complains = EcotrailManager.get_all_user_posts(user)
        # Use dump, not load when schema and object are not the same
        return ResponseEcotrailSchema().dump(complains, many=True)

    @auth.login_required
    @permission_required(RoleType.user)
    @validate_schema(RequestEcotrailSchema)
    def post(self):
        user = auth.current_user()
        data = request.get_json()
        ecotrail = EcotrailManager.create(data, user)
        # Use dump, not load when schema and object are not the same
        return ResponseEcotrailSchema().dump(ecotrail)


class EcotrailDetail(Resource):
    @auth.login_required
    @permission_required(RoleType.user)
    @validate_schema(RequestEcotrailSchema)
    def put(self, id_):
        updated_ecotrail = EcotrailManager.update(request.get_json(), id_)
        schema = ResponseEcotrailSchema()
        return schema.dump(updated_ecotrail)

    @auth.login_required
    @permission_required(RoleType.administrator)
    def delete(self, id_):
        EcotrailManager.delete(id_)
        return {"message": "Success"}, 204


class ApproveEcotrail(Resource):
    @auth.login_required
    @permission_required(RoleType.moderator)
    def put(self, id_):
        EcotrailManager.approve(id_)
        return 200


class RejectEcotrail(Resource):
    @auth.login_required
    @permission_required(RoleType.moderator)
    def put(self, id_):
        EcotrailManager.reject(id_)
        return 200
