import pickle
import mock
import time
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.notify import (
    Client,
    client_channel,
    user_channel,
)
from pynformatics.utils.redis import redis


class TestUtils__notify_client_get_message(TestCase):
    def setUp(self):
        super(TestUtils__notify_client_get_message, self).setUp()

        self.create_users()
        self.client = Client(user_id=self.users[0].id)
    
    def test_client_channel(self):
        channel = client_channel(self.client.uuid)
        data = pickle.dumps(123)

        redis.publish(channel, data)
        time.sleep(0.1)
        assert_that(self.client.get_message(), equal_to(123))
    
    def test_user_channel(self):
        channel = user_channel(self.users[0].id)
        data = pickle.dumps(123)

        redis.publish(channel, data)
        time.sleep(0.1)
        assert_that(self.client.get_message(), equal_to(123))
