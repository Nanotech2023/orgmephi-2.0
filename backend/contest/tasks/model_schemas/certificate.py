from marshmallow import validate
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
    certificate_category = EnumField(enum=UserStatusEnum, by_value=True, required=True)

    text_x = auto_field(required=True, description='Left border of textbox')
    text_y = auto_field(required=True, description='Bottom border of first line of text')
    text_width = auto_field(required=True, description='Textbox width')
    text_size = auto_field(required=False, load_default=14, description='Font size')
    text_style = auto_field(required=False, validate=common_name_validator,
                            load_default='DejaVuSans', example='DejaVuSans',
                            description='Text font, see /contest/tasks/admin/fonts for available fonts')
    text_spacing = auto_field(required=False, load_default=0, description='Distance between lines')
    text_color = auto_field(required=False, validate=validate.Regexp('^#[0-9,a-f]{8}$'), load_default='#ffffffff',
                            example='#ffffffff', description='#rrggbbaa color code')


class CertificateTypeSchema(SQLAlchemySchema):
    class Meta:
        model = CertificateType
        load_instance = True
        sqla_session = db.session

    certificate_type_id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=common_name_validator)
    description = auto_field(validate=text_validator)
    certificates = Nested(CertificateSchema, many=True, dump_only=True)
