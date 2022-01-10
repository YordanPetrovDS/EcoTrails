from datetime import datetime, timedelta

import jwt
from decouple import config
from flask_httpauth import HTTPTokenAuth
from models.enums import RoleType
from models.user import UserModel
from werkzeug.exceptions import BadRequest

mapper = {
    "administrator": lambda x: UserModel.query.filter_by(
        id=x, role=RoleType.administrator
    ).first(),
    "moderator": lambda x: UserModel.query.filter_by(
        id=x, role=RoleType.moderator
    ).first(),
    "user": lambda x: UserModel.query.filter_by(id=x, role=RoleType.user).first(),
}


class AuthManager:
    @staticmethod
    def encode_token(user,role):
        payload = {
            "sub": user.id,
            "exp": datetime.utcnow() + timedelta(days=100),
            "role": user.role.name,
        }
        return jwt.encode(payload, key=config("JWT_key"), algorithm="HS256")

    @staticmethod
    def decode_token(token):
        try:
            info = jwt.decode(jwt=token, key=config("JWT_key"), algorithms=["HS256"])
            return info["sub"], info["role"]
        except jwt.ExpiredSignatureError:
            raise BadRequest("Token is expired")
        except jwt.InvalidTokenError:
            raise BadRequest("Invalid token")


auth = HTTPTokenAuth(scheme="Bearer")


@auth.verify_token
def verify_token(token):
    user_id, role = AuthManager.decode_token(token)
    user = mapper[role](user_id)
    return user
