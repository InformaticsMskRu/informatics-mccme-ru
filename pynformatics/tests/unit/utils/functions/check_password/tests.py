from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.functions import check_password


class TestUtils__functions_check_password(TestCase):
    def test_matching(self):
        password = 'testtest'
        password_md5 = '05a671c66aefea124cc08b76ea6d30bb'

        assert_that(
            check_password(password, password_md5),
            equal_to(True),
        )

    def test_not_matching(self):
        password = 'testtest'
        password_md5 = '05a671c66aefea124cc08b76ea6d30bc'

        assert_that(
            check_password(password, password_md5),
            equal_to(False),
        )
