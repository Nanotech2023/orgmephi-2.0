from marshmallow import Schema, fields, validate
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum
from user.model_schemas.reference import UniversitySchema, CountrySchema, RegionSchema, CitySchema
from user.model_schemas.university import StudentUniversityCompatibleSchema
from user.model_schemas.location import LocationCompatibleSchema


class RegistrationInfoUserSchema(Schema):
    email = common_fields.Email(required=True)
    password = common_fields.Password(required=True)


class RegistrationPersonalInfoUserSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    second_name = common_fields.CommonName(required=True)
    middle_name = common_fields.CommonName(required=True)
    date_of_birth = fields.Date(required=True)


class RegisterConfirmUserSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class RegistrationStudentInfoUserSchema(Schema):
    phone = common_fields.Phone(required=True)
    grade = common_fields.Grade(required=True, validate=validate.Range(max=5))
    dwelling = fields.Nested(nested=LocationCompatibleSchema, required=True)
    university = fields.Nested(nested=StudentUniversityCompatibleSchema, required=True)


class SchoolRegistrationRequestUserSchema(Schema):
    auth_info = fields.Nested(nested=RegistrationInfoUserSchema, required=True)
    personal_info = fields.Nested(nested=RegistrationPersonalInfoUserSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.school,
                                                       UserTypeEnum.pre_university,
                                                       UserTypeEnum.enrollee]))
    register_confirm = fields.Nested(nested=RegisterConfirmUserSchema)


class UniversityRegistrationRequestUserSchema(Schema):
    auth_info = fields.Nested(nested=RegistrationInfoUserSchema, required=True)
    personal_info = fields.Nested(nested=RegistrationPersonalInfoUserSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.university]))
    student_info = fields.Nested(nested=RegistrationStudentInfoUserSchema, required=True)


class InfoUniversitiesResponseUserSchema(Schema):
    university_list = fields.Nested(UniversitySchema, many=True, required=True)


class InfoCountriesResponseUserSchema(Schema):
    country_list = fields.Nested(CountrySchema, many=True, required=True)


class InfoRegionsResponseUserSchema(Schema):
    region_list = fields.Nested(RegionSchema, many=True, required=True)


class InfoCitiesResponseUserSchema(Schema):
    city_list = fields.Nested(CitySchema, many=True, required=True)
