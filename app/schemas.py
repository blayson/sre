from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    email = fields.Email(required=True, description='User email for registration')
    password = fields.String(required=True, description='User password for registration')


class ReviewSchema(Schema):
    id = fields.Integer(dump_only=True)
    changed = fields.Boolean()
    user_id = fields.Integer(dump_only=True)


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=False, validate=[
        validate.Length(max=64)])
    email = fields.Email(required=True, validate=[
        validate.Length(max=120)])
    password = fields.String(required=True, validate=[
        validate.Length(max=128)], load_only=True)
    about_me = fields.String(validate=[
        validate.Length(max=120)])
    last_seen = fields.DateTime()
    reviews = fields.Nested(ReviewSchema, many=True, dump_only=True)


class AuthSchema(Schema):
    token = fields.String(dump_only=True)
    msg = fields.String(dump_only=True)
