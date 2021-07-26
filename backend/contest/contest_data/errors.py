from flask import make_response


class RequestError(Exception):
    def __init__(self, http_code=400):
        self.http_code = http_code

    def get_msg(self):
        return ''

    def to_response(self):
        return make_response({"errors": [
            {
                "class": str(type(self)),
                "status": self.http_code,
                "title": self.get_msg()
            }
        ]}, self.http_code)
