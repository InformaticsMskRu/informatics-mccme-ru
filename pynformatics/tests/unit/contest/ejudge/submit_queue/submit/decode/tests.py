import mock
import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.contest.ejudge.submit_queue.submit import Submit
from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context


class TestEjudge__submit_queue_submit_decode(TestCase):
    def test_simple(self):
        with mock.patch.object(Context, 'decode') as context_decode_mock:
            context_decode_mock.return_value = 'context'
            submit = Submit.decode({
                'id': 'id',
                'context': 'context',
                'create_time': datetime.datetime(2018, 3, 30, 17, 10, 11),
                'file': 'file',
                'language_id': 'language_id',
                'ejudge_url': 'ejudge_url',
            })
            context_decode_mock.assert_called_once_with('context')
            assert_that(submit.id, equal_to('id'))
            assert_that(submit.context, equal_to('context'))
            assert_that(submit.create_time, equal_to(datetime.datetime(2018, 3, 30, 17, 10, 11)))
            assert_that(submit.file, equal_to('file'))
            assert_that(submit.language_id, equal_to('language_id'))
            assert_that(submit.ejudge_url, equal_to('ejudge_url'))
