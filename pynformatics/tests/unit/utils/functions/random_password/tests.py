from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.functions import random_password


class TestUtils__functions_random_password(TestCase):
    def test_length(self):
        length = 10
        assert_that(
            len(random_password(length)),
            equal_to(length),
        )
