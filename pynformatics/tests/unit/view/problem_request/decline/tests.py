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
    ProblemRequestAlreadyReviewed,
    Unauthorized,
)
from pynformatics.testutils import TestCase

from pynformatics.view.problem_request import problem_request_decline


class TestView__problem_request_decline(TestCase):
    def setUp(self):
        super(TestView__problem_request_decline, self).setUp()

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
        self.problem_requests[1].status = ProblemRequestStatus.DECLINED.value

        self.session.add_all(self.problem_requests)
        self.session.flush()

    def test_simple(self):
        self.request.matchdict['problem_request_id'] = self.problem_requests[0].id
        self.request.json_body = {}
        context = Context(user_id=self.admin_user.user_id)

        response = problem_request_decline(self.request, context)
        query = DBSession.query(ProblemRequest).filter(ProblemRequest.id == self.problem_requests[0].id).first()

        assert_that(
            response,
            equal_to({})
        )
        assert_that(
            query.status,
            equal_to(ProblemRequestStatus.DECLINED.value)
        )

    def test_no_problem_request(self):
        self.request.matchdict['problem_request_id'] = 1000
        context = Context(user_id=self.admin_user.user_id)

        assert_that(
            calling(problem_request_decline).with_args(self.request, context),
            raises(ProblemRequestNotFound)
        )

    def test_already_reviewed(self):
        self.request.matchdict['problem_request_id'] = self.problem_requests[1].id
        self.request.json_body = {}
        context = Context(user_id=self.admin_user.user_id)

        assert_that(
            calling(problem_request_decline).with_args(self.request, context),
            raises(ProblemRequestAlreadyReviewed)
        )

    def test_not_admin(self):
        self.request.matchdict['problem_request_id'] = self.problem_requests[0].id
        context = Context(user_id=self.user.user_id)

        assert_that(
            calling(problem_request_decline).with_args(self.request, context),
            raises(Forbidden)
        )

    def test_unauthorized(self):
        context = Context(user_id=self.user.user_id + 1)

        assert_that(
            calling(problem_request_decline).with_args(None, context),
            raises(Unauthorized)
        )
