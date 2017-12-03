from hamcrest import (
    assert_that,
    has_entries,
    equal_to,
    calling,
    raises,
)
import mock

from pynformatics.testutils import TestCase
from pynformatics.model.user import User
from pynformatics.view.auth import auth_login
from pynformatics.utils.exceptions import AuthWrongUsernameOrPassword


class TestView__auth_login(TestCase):
    def setUp(self):
        super(TestView__auth_login, self).setUp()
        self.username = 'some username'
        self.password = 'testtest'
        self.password_md5 = '05a671c66aefea124cc08b76ea6d30bb'
        self.user = User(
            id=123,
            username=self.username,
            password_md5=self.password_md5,
        )
        self.session.add(self.user)

        self.request.json_body = {
            'username': self.username,
            'password': self.password,
        }

    def test_simple(self):
        with mock.patch('pynformatics.view.auth.check_password', mock.Mock(return_value=True)) as mock_check_password, \
                mock.patch('pynformatics.view.auth.moodle.sign_in', mock.Mock(return_value=(None, None))):
            result = auth_login(self.request)
        assert_that(
            result,
            has_entries({
                'id': self.user.id,
            })
        )
        assert_that(
            self.request.session,
            equal_to({
                'user_id': self.user.id,
            })
        )
        mock_check_password.assert_called_once_with(self.password, self.password_md5)

    def test_no_user(self):
        self.request.json_body['username'] = 'bad username'
        with mock.patch('pynformatics.view.auth.check_password', mock.Mock(return_value=True)), \
                mock.patch('pynformatics.view.auth.moodle.sign_in', mock.Mock(return_value=(None, None))):
            assert_that(
                calling(auth_login).with_args(self.request),
                raises(AuthWrongUsernameOrPassword),
            )
            assert_that(
                self.request.session,
                equal_to({})
            )

    def test_wrong_password(self):
        with mock.patch('pynformatics.view.auth.check_password', mock.Mock(return_value=False)), \
                mock.patch('pynformatics.view.auth.moodle.sign_in', mock.Mock(return_value=(None, None))):
            assert_that(
                calling(auth_login).with_args(self.request),
                raises(AuthWrongUsernameOrPassword),
            )
            assert_that(
                self.request.session,
                equal_to({})
            )

    def test_context_user(self):
        request = mock.Mock()
        request.session = {}
        context = mock.Mock()
        context.user = self.user
        result = auth_login(request=request, context=context)
        assert_that(
            result,
            has_entries({
                'id': self.user.id,
            })
        )
        assert_that(
            request.session,
            equal_to({
                'user_id': self.user.id,
            })
        )

