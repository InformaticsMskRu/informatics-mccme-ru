class BaseApiException(Exception):
    message = ''
    code = 500
    def __init__(self, message=None):
        if message:
            self.message = message


class BadRequest(BaseApiException):
    message = 'Bad Request'
    code = 400


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

class StatementNotVirtual(BadRequest):
    message = 'Not a virtual contest'

class StatementVirtualCanOnlyStartOnce(Forbidden):
    message = 'Can only start virtual contest once'

class StatementOnlyOneOngoingVirtual(Forbidden):
    message = 'Can only have one ongoing virtual contest'

class StatementNothingToFinish(Forbidden):
    message = 'No ongoing virtual contests'


class AuthWrongUsernameOrPassword(Forbidden):
    message = 'Wrong username or password'

class AuthOAuthUserNotFound(NotFound):
    message = 'No user with this OAuth'

class AuthOAuthBadProvider(BadRequest):
    message = 'Unknown OAuth provider'
