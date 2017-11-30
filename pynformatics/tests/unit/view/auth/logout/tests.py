from hamcrest import (
    assert_that,
    has_entries,
    calling,
    raises,
)
import mock

from pynformatics.testutils import TestCase
from pynformatics.model.user import User
from pynformatics.view.auth import auth_logout
from pynformatics.utils.exceptions import Unauthorized


class TestView__auth_logout(TestCase):
    def setUp(self):
        super(TestView__auth_logout, self).setUp()
        self.user = User()
        self.session.add(self.user)
        self.session.flush()

    def test_simple(self):
        with self.mock_context_check_auth:
            auth_logout(self.request)

    def test_logged_out(self):
        assert_that(
            calling(auth_logout).with_args(self.request),
            raises(Unauthorized),
        )
