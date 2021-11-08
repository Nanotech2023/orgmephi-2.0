from marshmallow import validate, post_load
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_enum import EnumField

from common.errors import InsufficientData, AlreadyExists
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
    certificate_year = auto_field(required=True, description='Academic year of the certificate')

    text_x = auto_field(required=True, description='Left border of textbox')
    text_y = auto_field(required=True, description='Bottom border of first line of text')
    text_width = auto_field(required=True, validate=validate.Range(0), description='Textbox width')
    text_size = auto_field(required=False, validate=validate.Range(1), load_default=14, description='Font size')
    text_style = auto_field(required=False, validate=common_name_validator,
                            load_default='DejaVuSans', example='DejaVuSans',
                            description='Text font, see /contest/tasks/admin/fonts for available fonts')
    text_spacing = auto_field(required=False, load_default=0, description='Distance between lines')
    text_color = auto_field(required=False, validate=validate.Regexp('^#[0-9,a-f]{8}$'), load_default='#ffffffff',
                            example='#ffffffff', description='#rrggbbaa color code')
    max_lines = auto_field(required=False, validate=validate.Range(1), load_default=None,
                           description='Maximum amount of lines')

    @post_load()
    def test_font(self, data, many, **kwargs):
        try:
            from PIL import ImageFont
            ImageFont.truetype(data.text_style)
        except OSError:
            raise InsufficientData('Font', data.text_style)
        return data


class CertificateTypeSchema(SQLAlchemySchema):
    class Meta:
        model = CertificateType
        load_instance = True
        sqla_session = db.session

    certificate_type_id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=common_name_validator)
    description = auto_field(validate=text_validator)
    certificates = Nested(CertificateSchema, many=True, dump_only=True)
