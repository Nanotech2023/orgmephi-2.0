from flask import request
from marshmallow import Schema, fields

from common import get_current_module

module = get_current_module()


class InputSchema(Schema):
    now = fields.DateTime(required=True)


class OutputSchema(Schema):
    msg = fields.Str(required=True)


class Output:
    def __init__(self, msg):
        self.msg = msg


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
        msg = 'Good morning'
    elif 12 <= time.hour < 18:
        msg = 'Good afternoon'
    elif 18 <= time.hour < 24:
        msg = 'Good evening'
    else:
        msg = 'ZzZzZ...'
    return Output(msg), 200
