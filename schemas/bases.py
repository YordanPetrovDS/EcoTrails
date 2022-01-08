from marshmallow import Schema, fields


class BaseEcotrailSchema(Schema):
    title = fields.String(required=True)
    description = fields.String(required=True)
    area = fields.String(required=True)
    mountain = fields.String(required=True)
    distance = fields.Float(required=True)
    difference_in_altitude = fields.Float(required=True)
    difficulty = fields.Integer(required=True)