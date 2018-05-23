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
from pynformatics.utils.exceptions import Forbidden, ProblemRequestNotFound, Unauthorized
from pynformatics.testutils import TestCase

from pynformatics.view.problem_request import problem_request_get


class TestAPI__problem_request_get(TestCase):
    def setUp(self):
        super(TestAPI__problem_request_get, self).setUp()

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

        self.problem_request = ProblemRequest(problem_id=1, user_id=2, name='name', content='content')
        self.session.add(self.problem_request)
        self.session.flush()

    def send_request(self,
                     problem_request_id=None,
                     session_user_id=None,
                     status_code=200):
        if session_user_id:
            self.set_session({'user_id': session_user_id})
        response = self.app.get(
            url = '/problem_request/{}'.format(problem_request_id),
            status = status_code,
        )
        return response

    def test_simple(self):
        response = self.send_request(
            problem_request_id=self.problem_request.id,
            session_user_id=self.admin_user.id,
        )

        context = Context(user_id=self.admin_user.user_id)
        query = DBSession.query(ProblemRequest).filter(ProblemRequest.id == self.problem_request.id).first()
        assert_that(
            response.json,
            equal_to(query.serialize(context))
        )

    def test_no_problem_request(self):
        response = self.send_request(
            problem_request_id=self.problem_request.id + 1,
            session_user_id=self.admin_user.id,
            status_code=404,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 404,
                'message': 'No problem request with this id',
            })
        )

    def test_not_admin(self):
        response = self.send_request(
            problem_request_id=self.problem_request.id,
            session_user_id=self.user.id,
            status_code=403,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Forbidden',
            })
        )

    def test_unauthorized(self):
        response = self.send_request(
            status_code=401,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 401,
                'message': 'Unauthorized',
            })
        )