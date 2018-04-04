import time
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.notify import (
    Client,
    notify_client,
    notify_user,
)
from pynformatics.utils.redis import redis


class TestUtils__notify_notify_client(TestCase):
    def setUp(self):
        super(TestUtils__notify_notify_client, self).setUp()

        self.create_users()
        self.client = Client(self.users[0].id)

    def test_simple(self):
        notify_client(self.client.uuid, message={'test': 123})
        assert_that(self.client.get_message(), equal_to({'test': 123}))


class TestUtils__notify_notify_user(TestCase):
    def setUp(self):
        super(TestUtils__notify_notify_user, self).setUp()

        self.create_users()
        self.client = Client(self.users[0].id)

    def test_simple(self):
        notify_user(self.users[0].id, message={'test': 123})
        time.sleep(0.1)
        assert_that(self.client.get_message(), equal_to({'test': 123}))
