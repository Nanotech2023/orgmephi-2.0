from marshmallow import Schema, fields, validate, post_load
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum
from user.model_schemas.reference import UniversitySchema, CountrySchema
from user.model_schemas.university import StudentUniversityCompatibleSchema


class AuthInfoRegistrationSchema(Schema):
    email = common_fields.Email(required=True)
    password = common_fields.Password(required=True)


class PersonalInfoRegistrationSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    second_name = common_fields.CommonName(required=True)
    middle_name = common_fields.CommonName(required=True)
    date_of_birth = fields.Date(required=True)


class RegisterConfirmRegistrationSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class StudentInfoRegistrationSchema(Schema):
    phone = common_fields.Phone(required=True)
    admission_year = fields.Date(required=True)
    citizenship = common_fields.CommonName(required=True)
    region = common_fields.CommonName(required=True)
    city = common_fields.CommonName(required=True)
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, required=True)


class SchoolRequestRegistrationSchema(Schema):
    auth_info = fields.Nested(nested=AuthInfoRegistrationSchema, required=True)
    personal_info = fields.Nested(nested=PersonalInfoRegistrationSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.school,
                                                       UserTypeEnum.pre_university,
                                                       UserTypeEnum.enrollee]))
    register_confirm = fields.Nested(nested=RegisterConfirmRegistrationSchema)


class UniversityRequestRegistrationSchema(Schema):
    auth_info = fields.Nested(nested=AuthInfoRegistrationSchema, required=True)
    personal_info = fields.Nested(nested=PersonalInfoRegistrationSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.university]))
    student_info = fields.Nested(nested=StudentInfoRegistrationSchema, required=True)


class InfoUniversitiesResponseRegistrationSchema(Schema):
    university_list = fields.Nested(UniversitySchema, many=True, required=True)


class InfoCountriesResponseRegistrationSchema(Schema):
    country_list = fields.Nested(CountrySchema, many=True, required=True)
