from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_oneofschema import OneOfSchema
from marshmallow_enum import EnumField
from marshmallow import fields, Schema, validate
from user.models.document import *
from common import fields as common_fields


class DocumentSchema(SQLAlchemySchema):
    class Meta:
        model = Document
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    document_type = EnumField(enum=DocumentTypeEnum, attribute='document_type', allow_none=True, by_value=True)
    document_name = fields.String(attribute='document_name', allow_none=True)
    series = auto_field(column_name='series', allow_none=True)
    number = auto_field(column_name='number', allow_none=True)
    issuer = auto_field(column_name='issuer', allow_none=True)
    issue_date = auto_field(column_name='issue_date', allow_none=True)
    code = fields.String(allow_none=True, description='Only for russian passport')


class DocumentRFCompatibleSchema(Schema):
    document_type = fields.String(required=True,
                                  validate=validate.OneOf([DocumentTypeEnum.rf_passport.value]))
    series = fields.String(validate=validate.Regexp('^[0-9]{4}$'), example='4520')
    number = fields.String(validate=validate.Regexp('^[0-9]{6}$'), example='123456')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()
    code = fields.String(validate=validate.Regexp('^[0-9]{3}-[0-9]{3}$'), example='123-456')


class DocumentRFInternationalCompatibleSchema(Schema):
    document_type = fields.String(required=True,
                                  validate=validate.OneOf([DocumentTypeEnum.rf_international_passport.value]))
    series = fields.String(validate=validate.Regexp('^[0-9]{2}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[0-9]{7}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentForeignPassportCompatibleSchema(Schema):
    document_type = fields.String(required=True,
                                  validate=validate.OneOf([DocumentTypeEnum.foreign_passport.value]))
    series = fields.String(validate=validate.Regexp('^[0-9]{1,16}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[0-9]{1,32}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentOtherCompatibleSchema(Schema):
    document_type = fields.String(required=True, validate=validate.OneOf([DocumentTypeEnum.other_document.value]))
    document_name = common_fields.CommonName(validate=validate.NoneOf(document_names.values()))
    series = fields.String(validate=validate.Regexp('^[0-9]{1,16}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[0-9]{1,32}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentCompatibleSchema(OneOfSchema):
    type_schemas = {DocumentTypeEnum.rf_passport.value: DocumentRFCompatibleSchema,
                    DocumentTypeEnum.rf_international_passport.value: DocumentRFInternationalCompatibleSchema,
                    DocumentTypeEnum.foreign_passport.value: DocumentForeignPassportCompatibleSchema,
                    DocumentTypeEnum.other_document.value: DocumentOtherCompatibleSchema}
    type_field = "document_type"
    type_field_remove = False

    def get_obj_type(self, obj):
        return getattr(obj, 'document_type', DocumentTypeEnum.other_document).value
