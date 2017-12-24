import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_entries,
    raises,
)

from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import UserNotFound

from pynformatics.view.user import user_reset_password


class TestView__user_reset_password(TestCase):
    def setUp(self):
        super(TestView__user_reset_password, self).setUp()

        self.password_md5 = 'some md5'
        self.user = User(password_md5=self.password_md5)

        self.session.add(self.user)
        self.session.flush()

    def test_simple(self):
        new_password = 'some password'
        self.request.json_body = {
            'id': self.user.id,
        }
        with self.mock_context_check_auth, \
             self.mock_context_check_roles, \
             mock.patch('pynformatics.view.user.User.reset_password', mock.Mock()) as mock_reset_password:
            mock_reset_password.return_value = new_password
            response = user_reset_password(self.request, None)

        mock_reset_password.assert_called_once()
        assert_that(
            response,
            has_entries({
                'id': self.user.id,
                'password': new_password,
            })
        )

    def test_no_user(self):
        self.request.json_body = {
            'id': 123,
        }
        with self.mock_context_check_auth, \
                self.mock_context_check_roles:
            assert_that(
                calling(user_reset_password).with_args(self.request),
                raises(UserNotFound)
            )
            assert_that(
                self.user.password_md5,
                equal_to(self.password_md5),
            )
