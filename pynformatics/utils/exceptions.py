class BaseApiException(Exception):
    message = ''
    code = 500
    def __init__(self, message=None):
        if message:
            self.message = message


class Unauthorized(BaseApiException):
    message = 'Unauthorized'
    code = 401


class Forbidden(BaseApiException):
    message = 'Forbidden'
    code = 403


class NotFound(BaseApiException):
    message = 'Not Found'
    code = 404


class StatementNotFound(NotFound):
    message = 'No statement with this id'