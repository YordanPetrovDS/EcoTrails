from sqlalchemy import func

from db import db
from models.enums import State


class EcotrailModel(db.Model):
    __tablename__ = "ecotrails"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(255), nullable=False)
    mountain = db.Column(db.String(255), nullable=False)
    distance = db.Column(db.Float, nullable=False)
    difference_in_altitude = db.Column(db.Integer)
    difficulty = db.Column(db.Integer, nullable=False)
    create_on = db.Column(db.DateTime, server_default=func.now())
    status = db.Column(db.Enum(State), default=State.pending, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("UserModel")
