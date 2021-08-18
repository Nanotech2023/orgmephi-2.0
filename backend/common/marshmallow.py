from typing import Type, Optional
from flask_sqlalchemy import Model
from marshmallow import ValidationError
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.schema import SQLAlchemySchema


def _enum_allowed_values(enum_type, validator):
    from marshmallow import validate
    if isinstance(validator, validate.OneOf):
        return {v for v in validator.choices}
    if isinstance(validator, validate.And):
        return _enum_allowed_values_list(enum_type, validator.validators)
    return set(enum_type)


def _enum_allowed_values_list(enum_type, validators):
    allowed = set(enum_type)
    for val in validators:
        dd = _enum_allowed_values(enum_type, val)
        allowed = allowed & _enum_allowed_values(enum_type, val)
    return allowed


def _enum2properties(self, field, **kwargs):
    import marshmallow_enum
    if isinstance(field, marshmallow_enum.EnumField):
        allowed = _enum_allowed_values_list(field.enum, field.validators)
        return {'type': 'string', 'enum': [m.value for m in field.enum if m in allowed]}
    return {}


def _related2properties(self, field, **kwargs):
    from marshmallow_sqlalchemy.fields import Related
    if isinstance(field, Related):
        return self.field2property(related_to_nested(field))
    return {}


def related_to_nested(field):
    """
    Converts a Related field to a corresponding Nested or a primitive field
    :param field: Related field
    :return: Converted Nested or primitive field
    """
    new_fields = {
        column: auto_field(required=True, model=field.related_model, column_name=column, validate=field.validators)
        for column in field.columns}

    class FieldSchema(SQLAlchemySchema.from_dict(new_fields)):
        class Meta:
            model = field.related_model

    args = ['dump_default', 'load_default', 'data_key', 'attribute', 'validate', 'required', 'allow_none',
            'load_only', 'dump_only', 'error_messages', 'metadata']

    kwargs = {arg: getattr(field, arg) for arg in args}

    if len(new_fields) > 1:
        kwargs.pop('dump_default')
        kwargs.pop('load_default')
        return Nested(nested=FieldSchema, **kwargs)
    elif len(new_fields) == 1:
        schema = FieldSchema()
        # noinspection PyUnresolvedReferences
        fld = schema.fields[field.columns[0]]
        for k, v in kwargs.items():
            setattr(fld, k, v)
        return fld
    else:
        raise TypeError(f'Related field has not columns: {repr(field)}')


def check_related_existence(data: dict, attribute: str, field: str, sqla_model: Type[Model],
                            table_field: Optional[str] = None) -> dict:
    """
    Ensures that a database object for a Related-type marshmallow-sqlalchemy field during pre_load
    :param data: Data for deserialization
    :param attribute: Name of the related attribute within marshmallow schema
    :param field: Name of the field by which the object is related within marshmallow schema
    :param sqla_model: SQLAlchemy model
    :param table_field: Name of the field by which the object is related within sqlalchemy model
    :return: Data for deserialization
    """
    from common.util import db_get_one_or_none
    from common.errors import NotFound
    if table_field is None:
        table_field = field
    obj = data.get(attribute, None)
    if isinstance(obj, dict):
        obj = obj.get(field, None)
    if obj is not None:
        if db_get_one_or_none(sqla_model, table_field, obj) is None:
            raise NotFound(f'{attribute}.{field}', str(obj))
    else:
        data.pop(attribute, None)
    return data


def require_fields(data: dict, fields: list[str]):
    """
    Checks if fields are present in the data
    :param data: Data dictionary to check
    :param fields: Fields to look for
    """
    for field in fields:
        if field not in data:
            raise ValidationError('Missing data for required field.', field, data)
