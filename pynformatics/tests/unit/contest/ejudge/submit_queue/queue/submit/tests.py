import mock
import sys
import tempfile
import time
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.contest.ejudge.submit_queue.submit import Submit
from pynformatics.contest.ejudge.submit_queue.queue import SubmitQueue
from pynformatics.utils.context import Context


class TestEjudge__submit_queue_submit_queue_submit(TestCase):
    def setUp(self):
        super(TestEjudge__submit_queue_submit_queue_submit, self).setUp()

        self.create_users()
        self.create_problems()

    def test_submit_get(self):
        queue = SubmitQueue(workers=0)
        assert_that(queue.total_in, equal_to(0))

        queue.submit(
            context=Context(user_id=1, problem_id=2),
            file='file',
            language_id='language_id',
            ejudge_url='ejudge_url',
        )
        assert_that(queue.total_in, equal_to(1))

        submit = queue.get()
        assert_that(submit.context.user_id, equal_to(1))
        assert_that(submit.context.problem_id, equal_to(2))

        assert_that(submit.file, equal_to('file'))
        assert_that(submit.language_id, equal_to('language_id'))
        assert_that(submit.ejudge_url, equal_to('ejudge_url'))

    def test_with_workers(self):
        file_mock = mock.Mock()
        file_mock.__reduce__ = lambda self: (mock.Mock, ())

        queue = SubmitQueue(workers=1)

        with mock.patch.object(Submit, 'send', autospec=True) as send_mock:
            queue.submit(
                context=Context(user_id=1, problem_id=2),
                file=file_mock,
                language_id='language_id',
                ejudge_url='ejudge_url',
            )
            assert_that(queue.total_in, equal_to(1))
            time.sleep(1)
            assert_that(queue.total_successful, equal_to(1))
            assert_that(send_mock.call_count, equal_to(1))

            submit_from_queue = send_mock.call_args[0][0]
            assert_that(submit_from_queue.context.user_id, equal_to(1))
            assert_that(submit_from_queue.context.problem_id, equal_to(2))
            assert_that(submit_from_queue.context.statement_id, equal_to(None))
            assert_that(submit_from_queue.language_id, equal_to('language_id'))
            assert_that(submit_from_queue.ejudge_url, equal_to('ejudge_url'))
