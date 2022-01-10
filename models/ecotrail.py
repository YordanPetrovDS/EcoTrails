from sqlalchemy import func

from db import db
from models.enums import State


class BaserEcotrailModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    mountain = db.Column(db.String(255), nullable=False)
    length = db.Column(db.Float, nullable=False)
    denivelation = db.Column(db.Integer)
    difficulty = db.Column(db.Integer, nullable=False)


class EcotrailModel(BaserEcotrailModel):
    __tablename__ = "ecotrails"
    create_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")


class EcotrailVisitedModel(BaserEcotrailModel):
    __tablename__ = "ecotrails_visited"
    ecotrail_id = db.Column(db.Integer, db.ForeignKey("ecotrails.id"))
    ecotrail = db.relationship("EcotrailModel")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")


class EcotrailPlannedModel(BaserEcotrailModel):
    __tablename__ = "ecotrails_planned"
    ecotrail_id = db.Column(db.Integer, db.ForeignKey("ecotrails.id"))
    ecotrail = db.relationship("EcotrailModel")
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")
