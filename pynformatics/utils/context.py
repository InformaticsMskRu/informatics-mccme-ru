from functools import wraps, partial

from pynformatics.model import (
    EjudgeProblem,
    SimpleUser,
    Statement,
)
from pynformatics.models import DBSession
from pynformatics.utils.constants import (
    LANG_NAME_BY_ID,
)
from pynformatics.view.utils import RequestGetUserId
from pynformatics.utils.exceptions import (
    UnauthorizedException,
)


class Context:
    def __init__(self, request):
        self._request = request

        self._user_id = RequestGetUserId(self._request)
        self._user = None

        self._problem_id = request.matchdict.get('problem_id')
        self._problem = None

        self._statement_id = request.matchdict.get('statement_id')
        self._statement = None

    @property
    def user_id(self):
        return self._user_id

    @property
    def user(self):
        if not self._user:
            self._user = DBSession.query(SimpleUser).filter(SimpleUser.id == self._user_id).first()
        return self._user

    @property
    def problem_id(self):
        return self._problem_id

    @property
    def problem(self):
        if not self._problem and self._problem_id:
            self._problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == self._problem_id).first()
        return self._problem

    @property
    def statement_id(self):
        return self._statement_id

    @property
    def statement(self):
        if not self._statement and self._statement_id:
            self._statement = DBSession.query(Statement).filter(Statement.id == self._statement_id).first()
        return self._statement

    def check_auth(self):
        if self._user_id == -1:
            raise UnauthorizedException

    def get_languages(self):
        """
        Returns dict (id -> language name) of allowed languages for this context
        """
        return LANG_NAME_BY_ID


def with_context(view_function=None, require_auth=False):
    """
    Passes context as additional argument to the view_function
    """
    if view_function is None:
        return partial(with_context, require_auth=False)

    @wraps(view_function)
    def wrapper(request):
        context = Context(request)
        if require_auth:
            context.check_auth()
        return view_function(request, context)
    return wrapper
