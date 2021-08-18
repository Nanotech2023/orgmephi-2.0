import enum
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Related, Nested
from marshmallow_oneofschema import OneOfSchema
from marshmallow import pre_load, validate, Schema
from marshmallow import fields
from user.models.university import *
from common.fields import CommonName
from common.marshmallow import check_related_existence


class StudentUniversityType(enum.Enum):
    known = 'Known'
    custom = 'Custom'


class StudentUniversityKnownSchema(SQLAlchemySchema):
    class Meta:
        model = StudentUniversityKnown
        load_instance = True
        sqla_session = db.session

    known_type = fields.String(validate=validate.OneOf([StudentUniversityType.known.value]), dump_only=True)
    university = Related(column=['name'], data_key='university', required=True)
    country = fields.String(dump_only=True)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_university(self, data, many, **kwargs):
        return check_related_existence(data, 'university', 'name', University)

    # noinspection PyUnusedLocal
    @pre_load()
    def pop_country(self, data, many, **kwargs):
        data.pop('country', None)
        return data


class StudentUniversityCustomSchema(SQLAlchemySchema):
    class Meta:
        model = StudentUniversityCustom
        load_instance = True
        sqla_session = db.session

    known_type = fields.String(validate=validate.OneOf([StudentUniversityType.custom.value]), dump_only=True)
    university = auto_field(column_name='university_name', required=True)
    country = Related(column=['name'], data_key='country', required=True)

    # noinspection PyUnusedLocal
    @pre_load()
    def check_university(self, data, many, **kwargs):
        check_related_existence(data, 'country', 'name', Country)
        return data


class StudentUniversitySchema(OneOfSchema):

    type_schemas = {StudentUniversityType.known.value: StudentUniversityKnownSchema,
                    StudentUniversityType.custom.value: StudentUniversityCustomSchema}
    type_field = "known_type"
    type_field_remove = False

    class_types = {StudentUniversityKnown: StudentUniversityType.known.value,
                   StudentUniversityCustom: StudentUniversityType.custom.value}

    def get_obj_type(self, obj):
        obj_type = self.class_types.get(type(obj), None)
        if obj_type is None:
            raise TypeError(f'Unknown object type: {obj.__class__.__name__}')
        return obj_type

    def get_data_type(self, data):
        from common.util import db_get_one_or_none
        if self.type_field in data and self.type_field_remove:
            data.pop(self.type_field)
        uni_name = data.get('university', None)
        if uni_name is not None:
            uni = db_get_one_or_none(University, 'name', uni_name)
            return StudentUniversityType.known.value if uni is not None else StudentUniversityType.custom.value
        return StudentUniversityType.custom.value


class StudentUniversityCompatibleSchema(Schema):
    university = CommonName(required=True)
    country = CommonName(required=False, description='Omit this field if university is known by backend')


class StudentInfoSchema(SQLAlchemySchema):
    class Meta:
        model = StudentInfo
        load_instance = True
        sqla_session = db.session

    user_id = auto_field(column_name='user_id', dump_only=True)
    phone = auto_field(column_name='phone', allow_none=True)
    university = Nested(nested=StudentUniversitySchema, allow_none=True, many=False)
    grade = fields.Integer(allow_none=True)
