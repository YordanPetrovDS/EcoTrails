import os
import uuid

from constants import TEMP_FILE_FOLDER
from db import db
from models import UserModel
from models.ecotrail import EcotrailModel
from models.enums import RoleType, State
from resources import ecotrail
from services.s3 import S3Service
from utils.helpers import decode_photo
from werkzeug.exceptions import NotFound

from managers.auth import auth

s3 = S3Service()


class EcotrailManager:
    @staticmethod
    def get_all_approved_posts(filters):
        if filters:
            ecotrails = (
                EcotrailModel.query.filter_by(**filters)
                .filter_by(status=State.approved)
                .all()
            )
        else:
            ecotrails = EcotrailModel.query.filter_by(status=State.approved).all()
        return ecotrails

    @staticmethod
    def get_all_user_posts(user):
        if isinstance(user, UserModel):
            return EcotrailModel.query.filter_by(user_id=user.id).all()
        return EcotrailModel.query.all()

    @staticmethod
    def create(data, user):
        """
        Decode the base64 encoded photo,
        uploads it to s3 and set the photo url to
        the s3 generated url.
        Creates a ecotrail.
        Flushes the rows.
        """
        data["user_id"] = user.id
        encoded_photo = data.pop("photo")
        extension = data.pop("photo_extension")
        name = f"{str(uuid.uuid4())}"
        path = os.path.join(TEMP_FILE_FOLDER, f"{name}.{extension}")

        try:
            decode_photo(encoded_photo, path)
            photo_url = s3.upload_photo(path, name, extension)
        except Exception as ex:
            raise ex
        finally:
            os.remove(path)

        data["photo_url"] = photo_url
        data["user_id"] = user.id

        ecotrail = EcotrailModel(**data)
        db.session.add(ecotrail)
        db.session.flush()
        return ecotrail

    @staticmethod
    def update(ecotrail_data, id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        if not ecotrail:
            raise NotFound("This ecotrail does not exist")
        user = auth.current_user()

        if not user.id == ecotrail.user_id:
            raise NotFound("This ecotrail does not exist")

        EcotrailModel.query.filter_by(id=id_).update(ecotrail_data)
        db.session.add(ecotrail)
        db.session.flush()
        return ecotrail

    @staticmethod
    def delete(id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        if not ecotrail:
            raise NotFound("This ecotrail does not exist")

        user = auth.current_user()
        if (user.role == RoleType.user and not user.id == ecotrail.user_id) or (
            user.role == RoleType.moderator and not user.id == ecotrail.user_id
        ):
            raise NotFound("This ecotrail does not exist")

        db.session.delete(ecotrail)
        db.session.flush()

    @staticmethod
    def approve(id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        if not ecotrail:
            raise NotFound("This ecotrail does not exist")

        EcotrailModel.query.filter_by(id=id_).update({"status": State.approved})
        db.session.add(ecotrail)
        db.session.flush()
        return ecotrail

    @staticmethod
    def reject(id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        if not ecotrail:
            raise NotFound("This ecotrail does not exist")

        EcotrailModel.query.filter_by(id=id_).update({"status": State.rejected})
        db.session.add(ecotrail)
        db.session.flush()
        return ecotrail
