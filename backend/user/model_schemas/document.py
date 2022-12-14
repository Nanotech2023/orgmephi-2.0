from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_oneofschema import OneOfSchema
from marshmallow_enum import EnumField
from marshmallow import fields, validate

from common import fields as common_fields

from user.models.document import *


class DocumentBaseSchema(SQLAlchemySchema):
    class Meta:
        model = Document
        load_instance = True
        sqla_session = db.session

    user_id = fields.Integer(dump_only=True)


class DocumentRFSchema(DocumentBaseSchema):
    document_type = EnumField(DocumentTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([DocumentTypeEnum.rf_passport]))
    document_name = common_fields.CommonName(dump_only=True)
    series = fields.String(validate=validate.Regexp('^[0-9]{4}$'), example='4520')
    number = fields.String(validate=validate.Regexp('^[0-9]{6}$'), example='123456')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()
    code = fields.String(validate=validate.Regexp('^[0-9]{3}-[0-9]{3}$'), example='123-456')
    insurance_policy = fields.String(validate=validate.Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$'), example='123-456-789 01')


class DocumentRFInternationalSchema(DocumentBaseSchema):
    document_type = EnumField(DocumentTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([DocumentTypeEnum.rf_international_passport]))
    document_name = common_fields.CommonName(dump_only=True)
    series = fields.String(validate=validate.Regexp('^[0-9]{2}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[0-9]{7}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentForeignPassportSchema(DocumentBaseSchema):
    document_type = EnumField(DocumentTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([DocumentTypeEnum.foreign_passport]))
    document_name = common_fields.CommonName(dump_only=True)
    series = fields.String(validate=validate.Regexp('^[a-zA-Z0-9]{1,16}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[a-zA-Z0-9]{1,32}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentBirthCertificateSchema(DocumentBaseSchema):
    document_type = EnumField(DocumentTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([DocumentTypeEnum.birth_certificate]))
    document_name = common_fields.CommonName(dump_only=True)
    series = fields.String(validate=validate.Regexp(
        '^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})-[\u0410-\u042F]{2}$'), example='III-????')
    number = fields.String(validate=validate.Regexp('^[0-9]{6}$'), example='123456')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()
    insurance_policy = fields.String(validate=validate.Regexp('^[0-9]{3}-[0-9]{3}-[0-9]{3} [0-9]{2}$'), example='123-456-789 01')


class DocumentOtherSchema(DocumentBaseSchema):
    document_type = EnumField(DocumentTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([DocumentTypeEnum.other_document]))
    document_name = common_fields.CommonName(validate=validate.NoneOf(document_names.values()))
    series = fields.String(validate=validate.Regexp('^[a-zA-Z0-9]{1,16}$'), example='12')
    number = fields.String(validate=validate.Regexp('^[a-zA-Z0-9]{1,32}$'), example='1234567')
    issuer = common_fields.FreeDescription()
    issue_date = fields.Date()


class DocumentSchema(OneOfSchema):
    type_schemas = {DocumentTypeEnum.rf_passport.value: DocumentRFSchema,
                    DocumentTypeEnum.rf_international_passport.value: DocumentRFInternationalSchema,
                    DocumentTypeEnum.foreign_passport.value: DocumentForeignPassportSchema,
                    DocumentTypeEnum.other_document.value: DocumentOtherSchema,
                    DocumentTypeEnum.birth_certificate.value: DocumentBirthCertificateSchema}
    type_field = "document_type"
    type_field_remove = False

    def get_obj_type(self, obj):
        return getattr(obj, 'document_type', DocumentTypeEnum.other_document).value
