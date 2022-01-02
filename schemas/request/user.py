from marshmallow import Schema, fields


class UserSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class RequestRegisterUserSchema(UserSchema):
    first_name = fields.String(min_length=2, max_length=20, required=True)
    last_name = fields.String(min_length=2, max_length=20, required=True)
    username = fields.String(min_length=7, max_length=15, required=True)


class RequestLoginUserSchema(UserSchema):
    pass


class RequestCreateAdminSchema(RequestRegisterUserSchema):
    pass


class RequestCreateModeratorSchema(RequestRegisterUserSchema):
    pass
