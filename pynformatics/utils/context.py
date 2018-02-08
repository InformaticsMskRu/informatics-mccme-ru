from functools import wraps, partial
from sqlalchemy import exists, join

from pynformatics.model.problem import EjudgeProblem
from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.models import DBSession
from pynformatics.utils.constants import (
    LANG_NAME_BY_ID,
)
from pynformatics.view.utils import RequestGetUserId
from pynformatics.utils.exceptions import (
    Forbidden,
    Unauthorized,
)
from source_tree.model.role import (
    Role,
    RoleAssignment,
)


class Context:
    REQUEST_KEYS = [
        'problem_id',
        'statement_id',
    ]

    def __init__(self, request):
        self._request = request

        if request.session.get('user_id'):
            self._user_id = request.session.get('user_id')
        else:
            self._user_id = RequestGetUserId(self._request)
            if self._user_id != -1:
                request.session['user_id'] = self._user_id
        self._user = None

        self._problem = None
        self._statement = None

        for request_key in self.REQUEST_KEYS:
            setattr(
                self,
                '_' + request_key,
                request.matchdict.get(request_key) or request.params.get(request_key)
            )

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id
        self._user = None

    @property
    def user(self):
        if not self._user:
            self._user = DBSession.query(User).filter(User.id == self._user_id).first()
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
        if self._user_id == -1 or not self.user:
            raise Unauthorized

    def check_roles(self, roles):
        """
        Проверяет наличие хотя бы одной роли у пользователя.
        :param roles: строка или несколько строк, обозначающих shortname ролей
        """
        if isinstance(roles, str):
            roles = (roles, )

        role_assignment_exist = DBSession.query(
            exists().select_from(
                join(RoleAssignment, Role)
            ).where(
                RoleAssignment.user_id == self.user_id
            ).where(
                Role.shortname.in_(roles)
            )
        ).scalar()

        if not role_assignment_exist:
            raise Forbidden

    def get_allowed_languages(self):
        """
        Returns dict (id -> language name) of allowed languages for this context
        """
        allowed_languages = set(LANG_NAME_BY_ID.keys())
        if self.statement:
            allowed_languages &= set(self.statement.get_allowed_languages() or allowed_languages)
        return {
            allowed_language: LANG_NAME_BY_ID[allowed_language]
            for allowed_language in allowed_languages
        }


def with_context(view_function=None,
                 require_auth=False,
                 require_roles=None,
                 ):
    """
    Passes context as additional argument to the view_function
    """
    if view_function is None:
        return partial(
            with_context,
            require_auth=require_auth,
            require_roles=require_roles,
        )

    @wraps(view_function)
    def wrapper(request, context=None):
        context = context or Context(request)
        if require_auth:
            context.check_auth()
        if require_roles:
            context.check_roles(require_roles)
        return view_function(request, context)
    return wrapper
