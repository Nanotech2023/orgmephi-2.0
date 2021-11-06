from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField
from common.fields import text_validator, common_name_validator

from contest.tasks.models.certificate import *


class CertificateSchema(SQLAlchemySchema):
    class Meta:
        model = Certificate
        load_instance = True
        sqla_session = db.session

    certificate_id = auto_field(dump_only=True)
    certificate_type_id = auto_field(dump_only=True)
    certificate_category = EnumField(enum=UserStatusEnum, by_value=True, dump_only=True)
    text_fields = auto_field(required=True)


class CertificateTypeSchema(SQLAlchemySchema):
    class Meta:
        model = CertificateType
        load_instance = True
        sqla_session = db.session

    certificate_type_id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=common_name_validator)
    description = auto_field(validate=text_validator)
    certificates = Nested(CertificateSchema, many=True, dump_only=True)
