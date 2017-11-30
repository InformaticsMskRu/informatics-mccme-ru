from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)
import mock

from pynformatics.model.user_oauth_provider import UserOAuthProvider
from pynformatics.testutils import TestCase
from pynformatics.view.auth import auth_oauth_login
from pynformatics.utils.exceptions import AuthOAuthUserNotFound


class TestView__auth_oauth_login(TestCase):
    def setUp(self):
        super(TestView__auth_oauth_login, self).setUp()

        self.provider = 'some provider'
        self.code = 'some code'
        self.request.json_body = {
            'provider': self.provider,
            'code': self.code,
        }

        self.user_id = 12345
        self.oauth_id = 'some oauth id'
        self.user_oauth_provider = UserOAuthProvider(
            user_id=self.user_id,
            provider=self.provider,
            oauth_id=self.oauth_id,
        )
        self.session.add(self.user_oauth_provider)

    def test_simple(self):
        with mock.patch('pynformatics.view.auth.get_oauth_id', mock.Mock(return_value=self.oauth_id)), \
                mock.patch('pynformatics.view.auth.auth_login') as mock_auth_login:
            auth_oauth_login(self.request)
        request, context = mock_auth_login.mock_calls[0][1]
        assert_that(
            context.user_id,
            equal_to(self.user_id)
        )

    def test_no_oauth_user(self):
        with mock.patch('pynformatics.view.auth.get_oauth_id', mock.Mock(return_value='unknown oauth_id')), \
                mock.patch('pynformatics.view.auth.auth_login') as mock_auth_login:
            assert_that(
                calling(auth_oauth_login).with_args(self.request),
                raises(AuthOAuthUserNotFound)
            )
