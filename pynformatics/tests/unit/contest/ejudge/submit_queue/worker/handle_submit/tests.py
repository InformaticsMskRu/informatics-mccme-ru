import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.contest.ejudge.submit_queue.worker import SubmitWorker
from pynformatics.testutils import TestCase


class TestEjudge__submit_queue_submit_worker_handle_submit(TestCase):
    def setUp(self):
        super(TestEjudge__submit_queue_submit_worker_handle_submit, self).setUp()

        self.submit_mock = mock.Mock()
        self.queue_mock = mock.Mock()
        self.queue_mock.get.return_value = self.submit_mock
        self.queue_mock.total_successful = 1
        self.queue_mock.total_failed = 2

    def test_successful(self):
        worker = SubmitWorker(self.queue_mock)
        worker.handle_submit()

        self.queue_mock.get.assert_called_once()
        self.submit_mock.send.assert_called_once()
        assert_that(self.queue_mock.total_successful, equal_to(2))
        assert_that(self.queue_mock.total_failed, equal_to(2))

    def test_failed(self):
        self.submit_mock.send.side_effect = lambda: 1 / 0

        worker = SubmitWorker(self.queue_mock)
        worker.handle_submit()

        self.queue_mock.get.assert_called_once()
        self.submit_mock.send.assert_called_once()
        assert_that(self.queue_mock.total_successful, equal_to(1))
        assert_that(self.queue_mock.total_failed, equal_to(3))
