from marshmallow import fields, validate
from marshmallow_enum import EnumField
from models.enums import State
from schemas.bases import BaseEcotrailSchema


class ResponseEcotrailSchema(BaseEcotrailSchema):
    id = fields.Integer(required=True)
    status = EnumField(State, by_value=True)
    create_on = fields.DateTime(required=True)
    photo_url = fields.String(required=True, validate=validate.Length(max=255))
