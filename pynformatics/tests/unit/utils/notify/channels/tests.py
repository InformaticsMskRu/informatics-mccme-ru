from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.notify import (
    client_channel,
    user_channel,
)


class TestUtils__notify_cnannels(TestCase):
    def test_client_channel(self):
        client_uuid = 'uuid'
        assert_that(client_channel(client_uuid), equal_to('notify:client:uuid'))
    
    def test_user_channel(self):
        user_id = 12547
        assert_that(user_channel(user_id), equal_to('notify:user:12547'))
