from hamcrest import (
    assert_that,
    equal_to,
)
import mock

from pynformatics.testutils import TestCase
from pynformatics.utils.oauth import fill_oauth_config_secrets


class TestUtils__oauth_fill_oauth_config_secrets(TestCase):
    def test_simple(self):
        mock_oauth_config = {
            'provider1': {
                'secret1': None,
                'secret_with_no_fill': None,
                'nonsecret1': 'nonsecret11',
            },
            'provider2': {
                'secret1': None,
                'nonsecret1': 'nonsecret21',
            }
        }
        settings = {
            'oauth.provider1.secret1': 'secret11',
            'oauth.provider2.secret1': 'secret21',
            'oauth.provider1.nonsecret1': 'secret3',
        }
        with mock.patch('pynformatics.utils.oauth.OAUTH_CONFIG', mock_oauth_config):
            fill_oauth_config_secrets(settings)

        assert_that(
            mock_oauth_config,
            equal_to({
                'provider1': {
                    'secret1': 'secret11',
                    'secret_with_no_fill': None,
                    'nonsecret1': 'nonsecret11',
                },
                'provider2': {
                    'secret1': 'secret21',
                    'nonsecret1': 'nonsecret21',
                }
            })
        )
