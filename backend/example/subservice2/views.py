from enum import Enum

from flask import request
from marshmallow import Schema, fields
from marshmallow_enum import EnumField, LoadDumpOptions

from common import get_current_module

module = get_current_module()


class InputSchema(Schema):
    now = fields.DateTime(required=True)


class TimeEnum(Enum):
    morning = 'morning'
    day = 'day'
    evening = 'evening'
    night = 'night'


class OutputSchema(Schema):
    msg = fields.Str(required=True, dump_only=True)
    time = EnumField(TimeEnum, required=True, dump_by=LoadDumpOptions.value)


class Output:
    def __init__(self, time):
        self.time = time

    @property
    def msg(self):
        if self.time == TimeEnum.morning:
            return 'Good morning'
        elif self.time == TimeEnum.day:
            return 'Good afternoon'
        elif self.time == TimeEnum.evening:
            return 'Good evening'
        elif self.time == TimeEnum.night:
            return 'ZzZzZ...'
        else:
            return '???'


@module.route('/hello', methods=['POST'], input_schema=InputSchema, output_schema=OutputSchema)
def hello():
    """
    Hello
    ---
    post:
        requestBody:
            content:
              application/json:
                schema: InputSchema
        responses:
            '200':
              description: OK
              content:
                application/json:
                  schema: OutputSchema
    """
    time = request.marshmallow['now']
    if 6 <= time.hour < 12:
        t = TimeEnum.morning
    elif 12 <= time.hour < 18:
        t = TimeEnum.day
    elif 18 <= time.hour < 24:
        t = TimeEnum.evening
    else:
        t = TimeEnum.night
    return Output(t), 200
