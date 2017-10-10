class BaseApiException(Exception):
    message = ''
    code = 500


class UnauthorizedException(BaseApiException):
    message = 'Unauthorized'
    code = 401
