from marshmallow import fields, validate
import re


def _limit_length(field, max_len):

    class LimitLength(field):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            validator = validate.Length(max=max_len)
            self.validators.insert(0, validator)

    return LimitLength


class _Phone(fields.String):
    PHONE_REGEX = re.compile(
        r'^([+]?\d[-.\s]??)?'
        r'(\d{2,3}[-.\s]??\d{2,3}[-.\s]??\d{2}[-.\s]??\d{2}|'
        r'\(\d{3}\)[-.\s]??\d{3}[-.\s]??\d{2}[-.\s]??\d{2}|'
        r'\d{3}[-.\s]??\d{2}[-.\s]??\d{2})$'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validator = validate.Regexp(self.PHONE_REGEX)
        self.validators.insert(0, validator)


Email = _limit_length(fields.Email, 64)


Phone = _limit_length(_Phone, 32)


Password = _limit_length(fields.String, 128)


Username = _limit_length(fields.String, 64)


CommonName = _limit_length(fields.String, 32)


GroupName = _limit_length(fields.String, 32)
