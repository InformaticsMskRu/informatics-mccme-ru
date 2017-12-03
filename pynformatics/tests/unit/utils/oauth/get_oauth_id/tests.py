from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)
import mock

from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import (
    AuthOAuthBadProvider,
    AuthOAuthUserNotFound,
)
from pynformatics.utils.oauth import get_oauth_id


class TestUtils__oauth_get_oauth_id(TestCase):
    def setUp(self):
        super(TestUtils__oauth_get_oauth_id, self).setUp()
        self.provider = 'some provider'
        self.code = 'secret'
        self.oauth_id = 'some oauth id'
        self.oauth_id_key = 'oauth id key'

        self.oauth_config = {
            self.provider: {
                'url': 'code: %(code)s; param: %(param)s',
                'method': 'get',
                'param': 'value',
                'oauth_id_key': self.oauth_id_key,
            }
        }

    def test_get_provider(self):
        get_response = mock.Mock()
        get_response.json = mock.Mock(return_value={self.oauth_id_key: self.oauth_id})
        with mock.patch('pynformatics.utils.oauth.requests.get', mock.Mock(return_value=get_response)) as mock_get, \
                mock.patch('pynformatics.utils.oauth.OAUTH_CONFIG', self.oauth_config):
            oauth_id = get_oauth_id(provider=self.provider, code=self.code)
        assert_that(
            oauth_id,
            equal_to(self.oauth_id)
        )
        mock_get.assert_called_once_with('code: secret; param: value')

    def test_post_provider(self):
        oauth_config = {
            self.provider: {
                'url': 'code: %(code)s; param: %(param)s',
                'method': 'post',
                'fields': ['a', 'b'],
                'param': 'value',
                'oauth_id_key': self.oauth_id_key,
                'a': 'A',
                'b': 'B',
            }
        }

        post_response = mock.Mock()
        post_response.json = mock.Mock(return_value={self.oauth_id_key: self.oauth_id})
        with mock.patch('pynformatics.utils.oauth.requests.post', mock.Mock(return_value=post_response)) as mock_post, \
                mock.patch('pynformatics.utils.oauth.OAUTH_CONFIG', oauth_config):
            oauth_id = get_oauth_id(provider=self.provider, code=self.code)
        assert_that(
            oauth_id,
            equal_to(self.oauth_id)
        )
        mock_post.assert_called_once_with(
            'code: %(code)s; param: %(param)s',
            data={
                'a': 'A',
                'b': 'B',
                'code': self.code,
            }
        )

    def test_url_profile(self):
        access_token = 'ijoijoiji'
        oauth_config = {
            self.provider: {
                'url': 'code: %(code)s; param: %(param)s',
                'url_profile': 'access_token: %(access_token)s',
                'method': 'get',
                'param': 'value',
                'oauth_id_key': self.oauth_id_key,
            }
        }

        get_response = mock.Mock()
        get_response.json = mock.Mock(
            side_effect=[
                {'access_token': access_token},
                {self.oauth_id_key: self.oauth_id}
            ]
        )
        with mock.patch('pynformatics.utils.oauth.requests.get', mock.Mock(return_value=get_response)) as mock_get, \
                mock.patch('pynformatics.utils.oauth.OAUTH_CONFIG', oauth_config):
            oauth_id = get_oauth_id(provider=self.provider, code=self.code)
        assert_that(
            oauth_id,
            equal_to(self.oauth_id)
        )
        token_call, profile_call = mock_get.mock_calls
        assert_that(
            token_call[1][0],
            equal_to('code: secret; param: value')
        )
        assert_that(
            profile_call[1][0],
            equal_to(oauth_config[self.provider]['url_profile'] % {'access_token': access_token})
        )

    def test_bad_provider(self):
        assert_that(
            calling(get_oauth_id).with_args(provider='bad provider', code='some code'),
            raises(AuthOAuthBadProvider)
        )
