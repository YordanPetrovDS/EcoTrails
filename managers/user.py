from db import db
from models.user import AdministratorModel, ModeratorModel, UserModel
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
                return AuthManager.encode_token(user)
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
            moderator = ModeratorModel.query.filter_by(email=user_data["email"]).first()
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
            admin = AdministratorModel.query.filter_by(email=user_data["email"]).first()
            if admin and check_password_hash(admin.password, user_data["password"]):
                return AuthManager.encode_token(admin)
            raise Exception
        except Exception:
            raise BadRequest("Invalid email or password")

    @staticmethod
    def create_admin(user_data):
        """
        Hashes the plain password
        :param user_data: dict
        :return: token
        """
        user_data["password"] = generate_password_hash(
            user_data["password"], method="sha256"
        )
        admin = AdministratorModel(**user_data)
        try:
            db.session.add(admin)
            db.session.flush()
            return AuthManager.encode_token(admin)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def create_moderator(user_data):
        """
        Hashes the plain password
        :param user_data: dict
        :return: token
        """
        user_data["password"] = generate_password_hash(
            user_data["password"], method="sha256"
        )
        moderator = ModeratorModel(**user_data)
        try:
            db.session.add(moderator)
            db.session.flush()
            return AuthManager.encode_token(moderator)
        except Exception as ex:
            raise BadRequest(str(ex))

    @staticmethod
    def delete_moderator(id_):
        moderator = ModeratorModel.query.filter_by(id=id_).first()
        if not moderator:
            raise NotFound("This moderator does not exist")
        db.session.delete(moderator)
        db.session.flush()
        return