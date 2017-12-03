from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_not,
    raises,
)
import mock

from pynformatics.model.user import User
from pynformatics.model.user_oauth_provider import UserOAuthProvider
from pynformatics.testutils import TestCase
from pynformatics.view.user import user_set_oauth_id
from pynformatics.utils.exceptions import (
    UserOAuthIdAlreadyUsed
)


class TestView__user_set_oauth_id(TestCase):
    def setUp(self):
        super(TestView__user_set_oauth_id, self).setUp()

        self.oauth_id1 = 'oauth_id1'
        self.oauth_id2 = 'oauth_id2'
        self.provider1 = 'provider1'
        self.provider2 = 'provider2'

        self.user = User(id=123)
        self.session.add(self.user)

        self.user_oauth_provider = UserOAuthProvider(
            user_id=self.user.id,
            provider=self.provider2,
            oauth_id=self.oauth_id2,
        )
        self.session.add(self.user_oauth_provider)

        self.request.json_body = {
            'provider': self.provider1,
            'code': 'some code',
        }

    def test_insert(self):
        with self.mock_context_user as mock_context_user, \
                mock.patch('pynformatics.view.user.get_oauth_id', mock.Mock(return_value=self.oauth_id1)), \
                self.mock_context_check_auth:
            mock_context_user.return_value = self.user
            user_set_oauth_id(self.request)
        created = self.session.query(UserOAuthProvider).filter(
            UserOAuthProvider.user_id == self.user.id
        ).filter(
            UserOAuthProvider.provider == self.provider1
        ).first()
        assert_that(
            created,
            is_not(None)
        )
        assert_that(
            created.oauth_id,
            equal_to(self.oauth_id1)
        )

    def test_update(self):
        self.request.json_body['provider'] = self.provider2
        with self.mock_context_user as mock_context_user, \
                mock.patch('pynformatics.view.user.get_oauth_id', mock.Mock(return_value=self.oauth_id1)), \
                self.mock_context_check_auth:
            mock_context_user.return_value = self.user
            user_set_oauth_id(self.request)
        created = self.session.query(UserOAuthProvider).filter(
            UserOAuthProvider.user_id == self.user.id
        ).filter(
            UserOAuthProvider.provider == self.provider2
        ).first()
        assert_that(
            created,
            is_not(None)
        )
        assert_that(
            created.oauth_id,
            equal_to(self.oauth_id1)
        )

    def test_oauth_id_used(self):
        self.request.json_body['provider'] = self.provider2
        with self.mock_context_user as mock_context_user, \
                mock.patch('pynformatics.view.user.get_oauth_id', mock.Mock(return_value=self.oauth_id2)), \
                self.mock_context_check_auth:
            mock_context_user.return_value = self.user
            assert_that(
                calling(user_set_oauth_id).with_args(self.request),
                raises(UserOAuthIdAlreadyUsed),
            )
