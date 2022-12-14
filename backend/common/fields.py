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
    r'\+[0-9]{10,17}$'
)

email_validator = validate.Length(max=64)
phone_validator = validate.And(validate.Length(max=32), validate.Regexp(PHONE_REGEX))
url_validator = validate.Length(max=128)
password_validator = validate.Length(max=128)
username_validator = validate.Length(max=64)
common_name_validator = validate.Length(max=32)
olympiad_name_validator = validate.Length(max=128)
group_name_validator = validate.Length(max=32)
text_validator = validate.Length(max=1024)
location_validator = validate.Length(max=128)
free_description_validator = validate.Length(max=256)
grade_validator = validate.Range(min=1)
message_validator = validate.Length(max=4096)
news_validator = validate.Length(max=4 * 1024 * 1024)  # 4 MB
user_answer_validator = validate.Length(max=2048)
condition_validator = validate.Range(min=0.0, max=1.0)
points_validator = validate.Range(min=0)
sequential_number_validator = validate.Range(min=1)
school_name_validator = validate.Length(max=128)

Email = _apply_validator(fields.Email, email_validator)
Phone = _add_example(_apply_validator(fields.String, phone_validator), '+78005553535')
URL = _add_example(_apply_validator(fields.URL, url_validator), 'https://www.example.com')
Password = _add_example(_apply_validator(fields.String, password_validator), 'qwertyA*1')
Username = _apply_validator(fields.String, username_validator)
CommonName = _apply_validator(fields.String, common_name_validator)
OlympiadName = _apply_validator(fields.String, olympiad_name_validator)
GroupName = _apply_validator(fields.String, group_name_validator)
Text = _apply_validator(fields.String, text_validator)
Location = _apply_validator(fields.String, location_validator)
FreeDescription = _apply_validator(fields.String, free_description_validator)
Grade = _apply_validator(fields.Integer, grade_validator)
Message = _apply_validator(fields.String, message_validator)
News = _apply_validator(fields.String, news_validator)
UserAnswer = _apply_validator(fields.String, user_answer_validator)
FloatCondition = _apply_validator(fields.Float, condition_validator)
SchoolName = _apply_validator(fields.String, school_name_validator)
# For Tasks and Contest

UserIds = _apply_validator(fields.String, group_name_validator)
