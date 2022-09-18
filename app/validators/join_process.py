from marshmallow import Schema, fields, post_load

from app.exceptions import RoleNotExistError, UserNotExistError
from app.models.user import User
from app.validators.custom_message import required_message
from app.validators.custom_validate import JoinValidate, object_id


class CreateInvitationSchema(Schema):
    user_id = fields.Str(
        required=True, validate=[object_id], error_messages={**required_message},
    )
    role_id = fields.Str(
        required=True, validate=[object_id], error_messages={**required_message},
    )
    message = fields.Str(
        required=True,
        validate=[JoinValidate.message_length],
        error_messages={**required_message},
    )

    @post_load
    def to_model(self, in_data):
        # 获取role和User
        in_data["role"] = (
            self.context["group"].role_cls.objects(id=in_data["role_id"]).first()
        )
        in_data["user"] = User.by_id(in_data["user_id"])
        # 如果缺少则抛出错误
        if in_data["role"] is None:
            raise RoleNotExistError
        if in_data["user"] is None:
            raise UserNotExistError
        return in_data


class SearchInvitationSchema(Schema):
    status = fields.List(fields.Int(), missing=None)


class SearchRelatedApplicationSchema(Schema):
    status = fields.List(fields.Int(), missing=None)


class ChangeInvitationSchema(Schema):
    role_id = fields.Str(required=True, error_messages={**required_message})


class CheckInvitationSchema(Schema):
    allow = fields.Boolean(required=True, error_messages={**required_message})


class SearchApplicationSchema(Schema):
    status = fields.List(fields.Int(), missing=None)


class CreateApplicationSchema(Schema):
    message = fields.Str(required=True, validate=[JoinValidate.message_length])


class CheckApplicationSchema(Schema):
    allow = fields.Boolean(required=True, error_messages={**required_message})
