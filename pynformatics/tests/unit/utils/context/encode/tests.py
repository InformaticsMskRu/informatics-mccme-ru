from hamcrest import (
    assert_that,
    equal_to
)

from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context


class TestUtils__context_encode(TestCase):
    def test_simple(self):
        context = Context(
            user_id=1,
            problem_id=2,
            statement_id=None,
        )
        assert_that(
            context.encode(),
            equal_to({
                'user_id': 1,
                'problem_id': 2,
                'statement_id': None,
            })
        )
