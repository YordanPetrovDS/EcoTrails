from marshmallow import fields
from schemas.bases import BaseEcotrailSchema


class RequestEcotrailSchema(BaseEcotrailSchema):
    photo = fields.String(required=True)
    photo_extension = fields.String(required=True)
