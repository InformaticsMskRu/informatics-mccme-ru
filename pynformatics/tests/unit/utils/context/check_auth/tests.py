import mock
from hamcrest import (
    assert_that,
    calling,
    raises,
)

from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import Unauthorized


class TestUtils__context_check_auth(TestCase):
    def setUp(self):
        super(TestUtils__context_check_auth, self).setUp()
        self.user = User()
        self.session.add(self.user)
        self.session.flush()

    def test_simple(self):
        self.request.session['user_id'] = self.user.id
        context = Context(self.request)
        context.check_auth()

    # def test_moodle_session(self):
    #     with mock.patch('pynformatics.utils.context.RequestGetUserId', mock.Mock(return_value=self.user.id)):
    #         context = Context(self.request)
    #     context.check_auth()

    def test_no_user_id(self):
        context = Context(self.request)
        assert_that(
            calling(context.check_auth),
            raises(Unauthorized)
        )

    def test_bad_user_id(self):
        self.request.session['user_id'] = 'bad user id'
        context = Context(self.request)
        assert_that(
            calling(context.check_auth),
            raises(Unauthorized)
        )