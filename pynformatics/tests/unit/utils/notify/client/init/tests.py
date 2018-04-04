import mock
from hamcrest import (
    assert_that,
    contains_inanyorder
)

from pynformatics.testutils import TestCase
from pynformatics.utils.notify import (
    Client,
    client_channel,
    user_channel,
)
from pynformatics.utils.redis import redis


class TestUtils__notify_client_init(TestCase):
    def test_subscribes_with_user(self):
        pubsub_mock = mock.Mock()
        with mock.patch.object(redis, 'pubsub', mock.Mock(return_value=pubsub_mock)):
            client = Client(user_id=1)
        calls = [
            call[0][0]
            for call in pubsub_mock.subscribe.call_args_list
        ]
        assert_that(
            calls,
            contains_inanyorder(
                client_channel(client.uuid),
                user_channel(1),
            )
        )
    
    def test_subscribes_without_user(self):
        pubsub_mock = mock.Mock()
        with mock.patch.object(redis, 'pubsub', mock.Mock(return_value=pubsub_mock)):
            client = Client()
        calls = [
            call[0][0]
            for call in pubsub_mock.subscribe.call_args_list
        ]
        assert_that(
            calls,
            contains_inanyorder(
                client_channel(client.uuid),
            )
        )
    
