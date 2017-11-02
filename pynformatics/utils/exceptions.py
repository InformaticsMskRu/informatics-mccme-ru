class BaseApiException(Exception):
    message = ''
    code = 500


class UnauthorizedException(BaseApiException):
    message = 'Unauthorized'
    code = 401


class NotFound(BaseApiException):
    message = 'Not Found'
    code = 404


class StatementNotFound(NotFound):
    message = 'No statement with this id'