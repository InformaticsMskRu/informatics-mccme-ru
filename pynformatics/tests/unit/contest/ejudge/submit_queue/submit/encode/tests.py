import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.contest.ejudge.submit_queue.submit import Submit
from pynformatics.testutils import TestCase


class TestEjudge__submit_queue_submit_encode(TestCase):
    def test_simple(self):
        context_mock = mock.Mock()
        context_mock.encode.return_value = 'context'
        submit = Submit(
            context=context_mock,
            file='file',
            language_id='language_id',
            ejudge_url='ejudge_url',
        )
        assert_that(
            submit.encode(),
            equal_to({
                'context': 'context',
                'file': 'file',
                'language_id': 'language_id',
                'ejudge_url': 'ejudge_url',
            })
        )
