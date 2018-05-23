import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)

from pynformatics import DBSession
from pynformatics.model.user import User
from source_tree.model.role import RoleAssignment
from pynformatics.model.problem_request import ProblemRequest
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import Forbidden, Unauthorized
from pynformatics.testutils import TestCase

from pynformatics.view.problem_request import problem_requests_get


class TestView__problem_requests_get(TestCase):
    def setUp(self):
        super(TestView__problem_requests_get, self).setUp()

        self.admin_user = User()
        self.admin_user.user_id = 1
        self.user = User()
        self.user.user_id = 2
        self.session.add_all((self.admin_user, self.user))
        self.session.flush()

        self.create_roles()
        self.role_assignment = RoleAssignment(user_id=self.admin_user.user_id, role=self.admin_role)
        self.session.add(self.role_assignment)
        self.session.flush()

        self.problem_requests = [ProblemRequest(problem_id=i, user_id=1, name='name', content='content')
                                 for i in range(3)]
        self.session.add_all(self.problem_requests)
        self.session.flush()

    def test_simple(self):
        context = Context(user_id=self.admin_user.user_id)

        response = problem_requests_get(None, context)
        query = DBSession.query(ProblemRequest)
        assert_that(
            response,
            equal_to([problem_request.serialize(context) for problem_request in query])
        )

    def test_not_admin(self):
        context = Context(user_id=self.user.user_id)

        assert_that(
            calling(problem_requests_get).with_args(None, context),
            raises(Forbidden)
        )

    def test_unauthorized(self):
        context = Context(user_id=self.user.user_id + 1)

        assert_that(
            calling(problem_requests_get).with_args(None, context),
            raises(Unauthorized)
        )