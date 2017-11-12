import mock
from hamcrest import (
    assert_that,
    equal_to,
    has_items,
)
from unittest.mock import PropertyMock

from pynformatics.testutils import TestCase
from pynformatics.utils.constants import LANG_NAME_BY_ID
from pynformatics.utils.context import Context


class TestContext__get_languages(TestCase):
    def setUp(self):
        super(TestContext__get_languages, self).setUp()

    def test__all(self):
        context = Context(self.request)
        assert_that(context.get_allowed_languages(), equal_to(LANG_NAME_BY_ID))

    def test__statement(self):
        allowed_languages = ['1', '2']
        mock_statement = mock.Mock()
        mock_statement.get_allowed_languages = mock.Mock(return_value=allowed_languages)
        with mock.patch.object(Context, 'statement', new_callable=PropertyMock) as mock_statement_property:
            mock_statement_property.return_value = mock_statement
            context = Context(self.request)
            assert_that(
                context.get_allowed_languages(),
                has_items(*allowed_languages)
            )
