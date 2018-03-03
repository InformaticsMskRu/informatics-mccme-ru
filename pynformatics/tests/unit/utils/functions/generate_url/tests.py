from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.url_generator import IntUrlGenerator


class TestUtils__functions_generate_url(TestCase):
    def test_int_url_generator(self):
        assert_that(IntUrlGenerator().encode(1), equal_to('867nv'))
