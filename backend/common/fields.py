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
free_description_validator = validate.Length(max=256)
grade_validator = validate.Range(min=1)
message_validator = validate.Length(max=4096)
news_validator = validate.Length(max=4*1024*1024)  # 4 MB

Email = _apply_validator(fields.Email, email_validator)
Phone = _add_example(_apply_validator(fields.String, phone_validator), '8 (800) 555 35 35')
Password = _add_example(_apply_validator(fields.String, password_validator), 'qwertyA*1')
Username = _apply_validator(fields.String, username_validator)
CommonName = _apply_validator(fields.String, common_name_validator)
GroupName = _apply_validator(fields.String, group_name_validator)
Text = _apply_validator(fields.String, text_validator)
Location = _apply_validator(fields.String, location_validator)
FreeDescription = _apply_validator(fields.String, free_description_validator)
Grade = _apply_validator(fields.Integer, grade_validator)
Message = _apply_validator(fields.String, message_validator)
News = _apply_validator(fields.String, news_validator)


# For Tasks and Contest

UserIds = _apply_validator(fields.String, group_name_validator)


class BytesField(fields.Field):
    def _validate(self, value):
        if not isinstance(value, bytes):
            raise ValidationError('Invalid input type.')

        if value is None or value == b'':
            raise ValidationError('Invalid value')
