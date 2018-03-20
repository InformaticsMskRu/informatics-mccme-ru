from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context


class TestUtils__context_decode(TestCase):
    def test_simple(self):
        context = Context.decode({
            'user_id': 1,
            'problem_id': 2,
            'statement_id': None,
        })
        assert_that(context.user_id, equal_to(1))
        assert_that(context.problem_id, equal_to(2))
        assert_that(context.statement_id, equal_to(None))
