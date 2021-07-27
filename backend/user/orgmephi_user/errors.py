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


class AlreadyExists(RequestError):
    def __init__(self, field, value):
        super(AlreadyExists, self).__init__(409)
        self.field = field
        self.value = value

    def get_msg(self):
        return '%s "%s" already exists' % (self.field, self.value)


class NotFound(RequestError):
    def __init__(self, field, value):
        super(NotFound, self).__init__(404)
        self.field = field
        self.value = value

    def get_msg(self):
        return '%s "%s" not found' % (self.field, self.value)


class WeakPassword(RequestError):
    def __init__(self, errors):
        super(WeakPassword, self).__init__(400)
        self.errors = errors

    def get_msg(self):
        return 'Password is too weak: %s' % str(self.errors)


class WrongCredentials(RequestError):
    def __init__(self):
        super(WrongCredentials, self).__init__(401)

    def get_msg(self):
        return 'Wrong credentials'
