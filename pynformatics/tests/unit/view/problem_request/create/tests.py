import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)
import transaction

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


class TestView__problem_request_create(TestCase):
    def setUp(self):
        super(TestView__problem_request_create, self).setUp()

        self.user = User()
        self.user.user_id = 1
        self.session.add(self.user)
        self.session.flush()

        self.create_problems()
        self.problem = self.problems[0]
        self.problem.name = 'Some name'
        self.problem.content = 'some content'

        self.context = Context(user_id=self.user.user_id)

    def test_simple(self):
        self.request.json_body = {
            'problem_id': self.problem.id,
            'name': 'New name',
            'content': 'New content',
        }

        assert_that(
            calling(create_problem_request).with_args(self.request, self.context),
            raises(transaction.interfaces.DoomedTransaction)
        )

        with mock.patch('transaction.commit') as mock_transaction:
            response = create_problem_request(self.request, self.context)
            query = DBSession.query(ProblemRequest).filter(ProblemRequest.id == 1).all()

            assert_that(
                response,
                has_entries({
                    'result': 'ok',
                })
            )
            assert_that(
                len(query),
                equal_to(1)
            )

    def test_no_problem(self):
        self.request.json_body = {
            'problem_id': 1000,
        }
        assert_that(
            calling(create_problem_request).with_args(self.request, self.context),
            raises(ProblemNotFound)
        )

    def test_no_changes(self):
        self.request.json_body = {
            'problem_id': self.problem.id,
            'name': self.problem.name,
            'content': self.problem.content,
        }
        assert_that(
            calling(create_problem_request).with_args(self.request, self.context),
            raises(ProblemRequestNoChanges)
        )

    def test_unauthorized(self):
        context = Context(user_id=self.user.user_id + 1)

        assert_that(
            calling(create_problem_request).with_args(None, context),
            raises(Unauthorized)
        )
