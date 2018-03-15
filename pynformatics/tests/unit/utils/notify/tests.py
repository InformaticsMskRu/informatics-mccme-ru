import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils import notify
from pynformatics.utils.notify import (
    Client,
    notify_user,
)

class TestUtils__notify_client(TestCase):
    def setUp(self):
        super(TestUtils__notify_client, self).setUp()
        notify._clients.clear()

    def test_init_adds_to_global_dict(self):
        client = Client(user_id=123)
        assert_that(notify._clients[123], equal_to([client]))

    def test_disconnect_removes_from_global_dict(self):
        client = Client(user_id=123)
        client.disconnect()
        assert_that(notify._clients[123], equal_to([]))

    def test_multiple_clients(self):
        # Создадим по три клиента для двух пользователей и отсоединим их
        clients = [
            Client(user_id=user_id)
            for user_id in range(2)
            for _ in range(3)
        ]
        assert_that(len(notify._clients), equal_to(2))
        assert_that(len(notify._clients[0]), equal_to(3))
        assert_that(len(notify._clients[1]), equal_to(3))

        clients[0].disconnect()
        clients[1].disconnect()
        assert_that(len(notify._clients[0]), equal_to(1))
        assert_that(len(notify._clients[1]), equal_to(3))

        clients[3].disconnect()
        clients[4].disconnect()
        clients[5].disconnect()
        assert_that(len(notify._clients[0]), equal_to(1))
        assert_that(len(notify._clients[1]), equal_to(0))

        clients[2].disconnect()
        assert_that(len(notify._clients[0]), equal_to(0))
        assert_that(len(notify._clients[1]), equal_to(0))

    def test_notify(self):
        client = Client(user_id=1)
        assert_that(client.has_notification(), equal_to(False))

        client.notify({'data': 123})
        assert_that(client.has_notification(), equal_to(True))
        assert_that(client.get_notification(), equal_to('{"data":123}'))
        assert_that(client.has_notification(), equal_to(False))


class TestUtils__notify_notify_user(TestCase):
    def setUp(self):
        super(TestUtils__notify_notify_user, self).setUp()
        notify._clients.clear()

    def test_notify_one_user(self):
        with mock.patch.object(Client, 'notify', autospec=True) as notify_mock:

            client1 = Client(user_id=1)
            client2 = Client(user_id=2)

            notify_user(1, 'data')

            notify_mock.assert_called_once_with(client1, 'data')

    def test_notify_no_client(self):
        with mock.patch.object(Client, 'notify', autospec=True) as notify_mock:
            notify_mock.side_effect = lambda self, data: (self.user_id, data)

            client1 = Client(user_id=1)
            client2 = Client(user_id=2)

            notify_user(3, 'data')
            assert_that(notify_mock.called, equal_to(False))

    def test_notify_multiple_clients(self):
        with mock.patch.object(Client, 'notify', autospec=True) as notify_mock:
            notify_mock.side_effect = lambda self, data: (self.user_id, data)

            client1_user1 = Client(user_id=1)
            client2_user1 = Client(user_id=1)
            client3_user1 = Client(user_id=1)

            client1_user2 = Client(user_id=2)
            client2_user2 = Client(user_id=2)

            notify_user(1, 'data')
            assert_that(notify_mock.call_count, equal_to(3))
