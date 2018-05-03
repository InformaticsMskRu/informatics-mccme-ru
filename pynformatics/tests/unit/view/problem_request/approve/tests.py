import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)
import transaction

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


class TestView__problem_request_approve(TestCase):
    def setUp(self):
        super(TestView__problem_request_approve, self).setUp()

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
                                 for i in range(3)]
        self.problem_requests[1].status = ProblemRequestStatus.DECLINED.value
        self.session.add_all(self.problem_requests)
        self.session.flush()


    def test_simple(self):
        self.request.json_body = {
            'problem_request_id': self.problem_requests[2].id,
        }
        context = Context(user_id=self.admin_user.user_id)

        assert_that(
            calling(problem_request_approve).with_args(self.request, context),
            raises(transaction.interfaces.DoomedTransaction)
        )

        self.request.json_body = {
            'problem_request_id': self.problem_requests[0].id,
        }

        with mock.patch('transaction.commit') as mock_transaction:
            problem_request = self.problem_requests[0]
            response = problem_request_approve(self.request, context)
            query = DBSession.query(ProblemRequest).filter(ProblemRequest.id == problem_request.id).first()
            problem = problem_request.get_problem().serialize(context)

            assert_that(
                response,
                has_entries({
                    'result': 'ok',
                })
            )
            assert_that(
                query.status,
                equal_to(ProblemRequestStatus.APPROVED.value)
            )
            assert_that(
                problem,
                has_entries({
                    'name': problem_request.name,
                    'content': problem_request.content,
                })
            )

    def test_no_problem_request(self):
        self.request.json_body = {
            'problem_request_id': 1000,
        }
        context = Context(user_id=self.admin_user.user_id)

        assert_that(
            calling(problem_request_approve).with_args(self.request, context),
            raises(ProblemRequestNotFound)
        )

    def test_already_reviewed(self):
        self.request.json_body = {
            'problem_request_id': self.problem_requests[1].id,
        }
        context = Context(user_id=self.admin_user.user_id)

        assert_that(
            calling(problem_request_approve).with_args(self.request, context),
            raises(ProblemRequestAlreadyReviewed)
        )

    def test_no_changes(self):
        self.request.json_body = {
            'problem_request_id': self.problem_requests[0].id,
            'name': self.problem.name,
            'content': self.problem.content,
        }
        context = Context(user_id=self.admin_user.user_id)
        assert_that(
            calling(problem_request_approve).with_args(self.request, context),
            raises(ProblemRequestNoChanges)
        )

    def test_not_admin(self):
        self.request.json_body = {
            'problem_request_id': self.problem_requests[0].id,
        }
        context = Context(user_id=self.user.user_id)

        assert_that(
            calling(problem_request_approve).with_args(self.request, context),
            raises(Forbidden)
        )

    def test_unauthorized(self):
        context = Context(user_id=self.user.user_id + 1)

        assert_that(
            calling(problem_request_approve).with_args(None, context),
            raises(Unauthorized)
        )
