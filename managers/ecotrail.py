from db import db
from models import UserModel
from models.ecotrail import EcotrailModel, EcotrailPlannedModel, EcotrailVisitedModel
from models.enums import RoleType, State
from utils.helpers import copy_ecotrail_to_respective_table, upload_photo_and_return_photo_url
from werkzeug.exceptions import NotFound

from managers.auth import auth


class EcotrailManager:
    @staticmethod
    def get_all_approved_posts(filters):
        ecotrails = EcotrailModel.query.filter(*filters).all()
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
        data = upload_photo_and_return_photo_url(data)
        data["user_id"] = user.id

        ecotrail = EcotrailModel(**data)
        db.session.add(ecotrail)
        db.session.flush()
        return ecotrail

    @staticmethod
    def update(data, id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        if not ecotrail:
            raise NotFound("This ecotrail does not exist")
        user = auth.current_user()

        if not user.id == ecotrail.user_id:
            raise NotFound("This ecotrail does not exist")

        data = upload_photo_and_return_photo_url(data)

        EcotrailModel.query.filter_by(id=id_).update(data)
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
        return

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

    @staticmethod
    def visited(id_):
        ecotrail = EcotrailModel.query.filter_by(id=id_).first()

        if ecotrail.status != State.approved:
            raise NotFound("This ecotrail is not approved, and should not be seen!")

        if not ecotrail:
            raise NotFound("This ecotrail does not exist")

        user = auth.current_user()

        ecotrail_dict = {
            c.name: getattr(ecotrail, c.name) for c in ecotrail.__table__.columns
        }

        ecotrail_dict["ecotrail_id"] = id_
        ecotrail_dict["user_id"] = user.id
        ecotrail_dict.pop("id")
        ecotrail_dict.pop("create_on")
        ecotrail_dict.pop("status")
        ecotrail_v = EcotrailVisitedModel(**ecotrail_dict)
        db.session.add(ecotrail_v)
        db.session.flush()
        return ecotrail_v

    @staticmethod
    def planned(id_):
        # ecotrail = EcotrailModel.query.filter_by(id=id_).first()
        user = auth.current_user()

        
        copy_ecotrail_to_respective_table(id_, user, EcotrailPlannedModel)
        
        # if ecotrail.status != State.approved:
        #     raise NotFound("This ecotrail is not approved, and should not be seen!")

        # if not ecotrail:
        #     raise NotFound("This ecotrail does not exist")

        
        # ecotrail_dict = {
        #     c.name: getattr(ecotrail, c.name) for c in ecotrail.__table__.columns
        # }

        # ecotrail_dict["ecotrail_id"] = id_
        # ecotrail_dict["user_id"] = user.id
        # ecotrail_dict.pop("id")
        # ecotrail_dict.pop("create_on")
        # ecotrail_dict.pop("status")
        # ecotrail_v = EcotrailPlannedModel(**ecotrail_dict)
        ecotrail_p = copy_ecotrail_to_respective_table(id_, user, EcotrailPlannedModel)
        db.session.add(ecotrail_p)
        db.session.flush()
        return ecotrail_p
