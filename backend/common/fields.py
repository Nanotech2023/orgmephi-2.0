from marshmallow import fields, validate, ValidationError
import re


def _apply_validator(field, validator):

    class ApplyValidator(field):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.validators.insert(0, validator)

    return ApplyValidator


def _add_example(field, example):

    class AddExample(field):

        def __init__(self, *args, **kwargs):
            kwargs['example'] = example
            super().__init__(*args, **kwargs)

    return AddExample


PHONE_REGEX = re.compile(
        r'^([+]?\d[-.\s]??)?'
        r'(\d{2,3}[-.\s]??\d{2,3}[-.\s]??\d{2}[-.\s]??\d{2}|'
        r'\(\d{3}\)[-.\s]??\d{3}[-.\s]??\d{2}[-.\s]??\d{2}|'
        r'\d{3}[-.\s]??\d{2}[-.\s]??\d{2})$'
    )


email_validator = validate.Length(max=64)
phone_validator = validate.And(validate.Length(max=32), validate.Regexp(PHONE_REGEX))
password_validator = validate.Length(max=128)
username_validator = validate.Length(max=64)
common_name_validator = validate.Length(max=32)
group_name_validator = validate.Length(max=32)
text_validator = validate.Length(max=1024)
location_validator = validate.Length(max=128)


Email = _apply_validator(fields.Email, email_validator)
Phone = _add_example(_apply_validator(fields.String, phone_validator), '8 (800) 555 35 35')
Password = _add_example(_apply_validator(fields.String, password_validator), 'qwertyA*1')
Username = _apply_validator(fields.String, username_validator)
CommonName = _apply_validator(fields.String, common_name_validator)
GroupName = _apply_validator(fields.String, group_name_validator)
Text = _apply_validator(fields.String, text_validator)
Location = _apply_validator(fields.String, location_validator)

# For Tasks and Contest

UserIds = _apply_validator(fields.String, group_name_validator)


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')
