from typing import Type
from marshmallow_sqlalchemy.fields import Nested
from marshmallow_sqlalchemy import auto_field
from marshmallow_sqlalchemy.schema import SQLAlchemySchema
from .errors import NotFound


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


def db_update_from_dict(db_session, data: dict, obj, schema: Type[SQLAlchemySchema]):
    """
    Update a database object from a dictionary based on a marshmallow schema
    :param db_session: Database session
    :param data: Dictionary of model attributes
    :param obj: Database object to update
    :param schema: marshmallow schema for the database model
    """
    from marshmallow_sqlalchemy.fields import Related, RelatedList
    from marshmallow.fields import Nested
    from marshmallow_oneofschema import OneOfSchema
    from sqlalchemy.orm import RelationshipProperty, ColumnProperty
    from sqlalchemy.inspection import inspect
    sch = schema()
    model = type(obj)
    model_info = inspect(model)
    for key, value in data.items():
        fld = sch.fields.get(key, None)
        if fld is None:
            raise ValueError(f'Field {key} not found in schema {schema.__class__}')
        if fld.attribute is not None:
            attr_name = fld.attribute
        else:
            attr_name = key
        column = getattr(model_info.attrs, attr_name, None)
        if column is None:
            raise ValueError(f'Attribute {attr_name} not found in model {model.__class__}')
        if value is None:
            setattr(obj, attr_name, None)
            continue
        if isinstance(fld, Related) and isinstance(column, RelationshipProperty):
            relation = getattr(model_info.relationships, attr_name, None)
            other_model = relation.mapper.class_
            if isinstance(value, other_model):
                value_info = inspect(value)
                if value_info.transient:
                    raise NotFound(f'{key} {str(fld.columns)}', str([getattr(value, k) for k in fld.columns]))
                setattr(obj, key, value)
            else:
                if value is dict:
                    filters = value
                else:
                    filters = {fld.columns[0]: value}
                rel = db_session.query(other_model).filter_by(**filters).one_or_none()
                if rel is None:
                    raise NotFound(key, str(value))
                setattr(obj, attr_name, rel)
        elif isinstance(fld, RelatedList) and isinstance(column, RelationshipProperty):
            pass
        elif isinstance(fld, Nested) and isinstance(column, RelationshipProperty):
            relation = getattr(model_info.relationships, attr_name, None)
            other_model = relation.mapper.class_
            nested = fld.nested
            if issubclass(nested, OneOfSchema):
                nested = nested.type_schemas[nested().get_data_type(value)]
                nested_model = nested.Meta.model
                nested_value = getattr(obj, attr_name)
                if not isinstance(nested_value, nested_model):
                    setattr(obj, attr_name, nested_model())
                other_model = nested_model
            elif getattr(obj, attr_name) is None:
                setattr(obj, attr_name, other_model())
            db_update_from_dict(db_session, value, getattr(obj, attr_name), nested)
        elif isinstance(column, ColumnProperty):
            setattr(obj, attr_name, value)
        else:
            raise TypeError(f'Unknown type for attribute {attr_name}')
