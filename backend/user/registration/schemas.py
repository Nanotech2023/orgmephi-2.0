from marshmallow import Schema, fields, post_load, validate
from marshmallow_enum import EnumField
from common import fields as common_fields
from user.models.auth import UserTypeEnum, user_types
from user.model_schemas.auth import UserSchema
from user.model_schemas.reference import UniversitySchema, CountrySchema


class AuthInfoSchema(Schema):
    email = common_fields.Email(required=True)
    password = common_fields.Password(required=True)


class PersonalInfoSchema(Schema):
    first_name = common_fields.CommonName(required=True)
    second_name = common_fields.CommonName(required=True)
    middle_name = common_fields.CommonName(required=True)
    date_of_birth = fields.Date(required=True)


class RegisterConfirmSchema(Schema):
    registration_number = common_fields.Username(required=True)
    password = common_fields.Password(required=True)


class StudentInfoRegistrationSchema(Schema):
    phone = common_fields.Phone(required=True)
    university = common_fields.CommonName(required=True)
    admission_year = fields.Date(required=True)
    university_country = common_fields.CommonName(required=True)
    citizenship = common_fields.CommonName(required=True)
    region = common_fields.CommonName(required=True)
    city = common_fields.CommonName(required=True)


class SchoolRequestSchema(Schema):
    auth_info = fields.Nested(nested=AuthInfoSchema, required=True)
    personal_info = fields.Nested(nested=PersonalInfoSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.school,
                                                       UserTypeEnum.pre_university,
                                                       UserTypeEnum.enrollee]))
    register_confirm = fields.Nested(nested=RegisterConfirmSchema)

    @post_load()
    def convert_enum(self, item, many, **kwargs):
        val = item.get('register_type', None)
        if val is not None:
            item['register_type'] = user_types[val.value]
        return item


SchoolResponseSchema = UserSchema


class UniversityRequestSchema(Schema):
    auth_info = fields.Nested(nested=AuthInfoSchema, required=True)
    personal_info = fields.Nested(nested=PersonalInfoSchema, required=True)
    register_type = EnumField(UserTypeEnum, by_value=True, required=True,
                              validate=validate.OneOf([UserTypeEnum.university]))
    student_info = fields.Nested(nested=StudentInfoRegistrationSchema, required=True)


UniversityResponseSchema = UserSchema


class InfoUniversitiesResponseSchema(Schema):
    university_list = fields.Nested(UniversitySchema, many=True, required=True)


class InfoCountriesResponseSchema(Schema):
    country_list = fields.Nested(CountrySchema, many=True, required=True)
