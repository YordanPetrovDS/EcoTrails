from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6, max=255))


class RequestRegisterUserSchema(UserSchema):
    first_name = fields.String(required=True, validate=validate.Length(min=2, max=255))
    last_name = fields.String(required=True, validate=validate.Length(min=2, max=255))


class RequestLoginUserSchema(UserSchema):
    pass


class RequestCreateAdminSchema(RequestRegisterUserSchema):
    pass


class RequestCreateModeratorSchema(RequestRegisterUserSchema):
    pass
