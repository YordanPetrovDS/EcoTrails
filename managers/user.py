from db import db
from models.enums import RoleType
from models.user import UserModel
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from managers.auth import AuthManager


class UserManager:
    @staticmethod
    def register_user(user_data):
        """
        Hashes the plain password
        :param user_data: dict
        :return: token
        """
        user_data["password"] = generate_password_hash(user_data["password"])
        user = UserModel(**user_data)
        db.session.add(user)
        db.session.flush()
        return AuthManager.encode_token(user)

    @staticmethod
    def login_user(user_data):
        """
        Checks the email and password (hashes the plain password)
        :param user_data: dict -> email, password
        :return: token
        """
        try:
            user = UserModel.query.filter_by(email=user_data["email"]).first()
            if user and check_password_hash(user.password, user_data["password"]):
                return AuthManager.encode_token(user), user.role.value
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")

    @staticmethod
    def login_moderator(user_data):
        """
        Checks the email and password (hashes the plain password)
        :param user_data: dict -> email, password
        :return: token
        """
        try:
            moderator = UserModel.query.filter_by(
                email=user_data["email"], role=RoleType.moderator
            ).first()
            if moderator and check_password_hash(
                moderator.password, user_data["password"]
            ):
                return AuthManager.encode_token(moderator)
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")

    @staticmethod
    def login_admin(user_data):
        """
        Checks the email and password (hashes the plain password)
        :param user_data: dict -> email, password
        :return: token
        """
        try:
            admin = UserModel.query.filter_by(
                email=user_data["email"], role=RoleType.administrator
            ).first()
            if admin and check_password_hash(admin.password, user_data["password"]):
                return AuthManager.encode_token(admin)
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")

    @staticmethod
    def create_admin(id_):
        user = UserModel.query.filter_by(id=id_).first()
        if not user:
            raise NotFound("This user does not exist")
        if user.role == RoleType.moderator:
            raise BadRequest("This user is already an admin")

        UserModel.query.filter_by(id=id_).update({"role": RoleType.administrator})
        db.session.add(user)
        db.session.flush()
        return user

    @staticmethod
    def create_moderator(id_):
        user = UserModel.query.filter_by(id=id_).first()
        if not user:
            raise NotFound("This user does not exist")
        if user.role == RoleType.moderator:
            raise BadRequest("This user is already a moderator")

        UserModel.query.filter_by(id=id_).update({"role": RoleType.moderator})
        db.session.add(user)
        db.session.flush()
        return user

    @staticmethod
    def demote_moderator(id_):
        moderator = UserModel.query.filter_by(id=id_, role="moderator").first()
        if not moderator:
            raise NotFound("This moderator does not exist")

        UserModel.query.filter_by(id=id_, role="moderator").update(
            {"role": RoleType.user}
        )
        db.session.add(moderator)
        db.session.flush()
        return moderator
