class BaseApiException(Exception):
    message = ''
    code = 500

    def __init__(self, message=None):
        if message:
            self.message = message

    def __str__(self):
        return self.message


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

class StatementCanOnlyStartOnce(Forbidden):
    message = 'Can only start contest once'

class StatementOnlyOneOngoing(Forbidden):
    message = 'Can only have one ongoing contest'

class StatementNothingToFinish(Forbidden):
    message = 'No ongoing virtual contests'

class StatementNotOlympiad(BadRequest):
    message = 'Not an olympiad'

class StatementFinished(Forbidden):
    message = 'Contest already finished'

class StatementNotStarted(Forbidden):
    message = 'Contest not started'

class StatementSettingsValidationError(BadRequest):
    message = 'Invalid settings format'


class AuthWrongUsernameOrPassword(Forbidden):
    message = 'Wrong username or password'

class AuthOAuthUserNotFound(NotFound):
    message = 'No user with this OAuth ID'

class AuthOAuthBadProvider(BadRequest):
    message = 'Unknown OAuth provider'

class UserOAuthIdAlreadyUsed(Forbidden):
    message = 'OAuth ID already in use'

class UserNotFound(NotFound):
    message = 'No such user'

class SearchQueryIsEmpty(BadRequest):
    message = 'Search query is empty'


class PaginationPageOutOfRange(BadRequest):
    message = 'Page number is out of range'

class PaginationPageSizeNegativeOrZero(BadRequest):
    message = 'Page size is negative or zero'

