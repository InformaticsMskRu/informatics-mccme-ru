import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)

from pynformatics import DBSession
from source_tree.model.role import RoleAssignment
from pynformatics.model.user import User
from pynformatics.model.problem_request import ProblemRequest, ProblemRequestStatus
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import (
    Forbidden,
    ProblemRequestNotFound,
    ProblemRequestNoChanges,
    ProblemRequestAlreadyReviewed,
    Unauthorized,
)
from pynformatics.testutils import TestCase

from pynformatics.view.problem_request import problem_request_approve


class TestAPI__problem_request_approve(TestCase):
    def setUp(self):
        super(TestAPI__problem_request_approve, self).setUp()

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

        self.create_problems()
        self.problem = self.problems[0]
        self.problem.name = 'Some name'
        self.problem.content = 'some content'

        self.problem_requests = [ProblemRequest(problem_id=self.problems[i].id, user_id=1, name='name', content='content')
                                 for i in range(2)]
        self.problem_requests[1].status = ProblemRequestStatus.DECLINED.value
        self.session.add_all(self.problem_requests)
        self.session.flush()

    def send_request(self,
                     problem_request_id=None,
                     name=None,
                     content=None,
                     session_user_id=None,
                     status_code=200,
                     ):
        if session_user_id:
            self.set_session({'user_id': session_user_id})
        response = self.app.post_json(
            url='/problem_request_approve',
            params={
                'problem_request_id': problem_request_id,
                'name': name,
                'content': content,
            },
            status=status_code,
        )
        return response

    def test_simple(self):
        with mock.patch('transaction.commit') as mock_transaction:
            response = self.send_request(
                problem_request_id=self.problem_requests[0].id,
                content='New content',
                name='New name',
                session_user_id=self.admin_user.id,
            )
            assert_that(
                response.json,
                has_entries({
                    'result': 'ok',
                })
            )

    def test_no_problem_request(self):
        response = self.send_request(
            problem_request_id=1000,
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

    def test_already_reviewed(self):
        response = self.send_request(
            problem_request_id=self.problem_requests[1].id,
            session_user_id=self.admin_user.id,
            status_code=400,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 400,
                'message': 'Problem request is already reviewed',
            })
        )

    def test_no_changes(self):
        response = self.send_request(
            problem_request_id=self.problem_requests[0].id,
            name=self.problem.name,
            content=self.problem.content,
            session_user_id=self.admin_user.id,
            status_code=400,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 400,
                'message': 'No changes in the problem request',
            })
        )

    def test_not_admin(self):
        response = self.send_request(
            problem_request_id=self.problem_requests[0].id,
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