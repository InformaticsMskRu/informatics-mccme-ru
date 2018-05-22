import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)

from pynformatics import DBSession, EjudgeProblem, User
from pynformatics.model.problem_request import ProblemRequest
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import (
    ProblemNotFound,
    ProblemRequestNoChanges,
    Unauthorized
)
from pynformatics.testutils import TestCase

from pynformatics.view.problem_request import create_problem_request


class TestAPI__problem_request_create(TestCase):
    def setUp(self):
        super(TestAPI__problem_request_create, self).setUp()

        self.user = User()
        self.user.user_id = 1
        self.session.add(self.user)
        self.session.flush()

        self.create_problems()
        self.problem = self.problems[0]
        self.problem.name = 'Some name'
        self.problem.content = 'some content'

        self.context = Context(user_id=self.user.user_id)

    def send_request(self,
                     problem_id=None,
                     name=None,
                     content=None,
                     session_user_id=None,
                     status_code=200,
                     ):
        if session_user_id:
            self.set_session({'user_id': session_user_id})
        response = self.app.post_json(
            url='/problem_request',
            params={
                'problem_id': problem_id,
                'name': name,
                'content': content,
            },
            status=status_code,
        )
        return response

    def test_simple(self):
        with mock.patch('transaction.commit') as mock_transaction:
            response = self.send_request(
                problem_id=self.problem.id,
                name='New name',
                content='New content',
                session_user_id=self.user.id,
            )
            assert_that(
                response.json,
                equal_to({})
            )

    def test_no_problem(self):
        response = self.send_request(
            problem_id=1000,
            session_user_id=self.user.id,
            status_code=404,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 404,
                'message': 'No problem with this id',
            })
        )

    def test_no_changes(self):
        response = self.send_request(
            problem_id=self.problem.id,
            name=self.problem.name,
            content=self.problem.content,
            session_user_id=self.user.id,
            status_code=400,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 400,
                'message': 'No changes in the problem request',
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