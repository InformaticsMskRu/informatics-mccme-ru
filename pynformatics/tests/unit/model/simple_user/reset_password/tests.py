import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.model.user import SimpleUser


class TestModel__simple_user_rest_password(TestCase):
    def setUp(self):
        super(TestModel__simple_user_rest_password, self).setUp()

        self.simple_user = SimpleUser()
        self.session.add(self.simple_user)

    def test_simple(self):
        password = 'some password'
        hashed_password = 'hashed password'
        with mock.patch('pynformatics.model.user.random_password', mock.Mock(return_value=password)), \
                mock.patch('pynformatics.model.user.hash_password', mock.Mock(return_value=hashed_password)):
            assert_that(
                self.simple_user.reset_password(),
                equal_to(password)
            )
            assert_that(
                self.simple_user.password_md5,
                equal_to(hashed_password)
            )
