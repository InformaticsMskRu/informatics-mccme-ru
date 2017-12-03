import mock
from hamcrest import (
    assert_that,
    equal_to,
    has_items,
    calling,
    raises,
)
from unittest.mock import PropertyMock

from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.constants import LANG_NAME_BY_ID
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import Unauthorized


class TestUtils__context_get_languages(TestCase):
    def setUp(self):
        super(TestUtils__context_get_languages, self).setUp()

    def test_all(self):
        context = Context(self.request)
        assert_that(context.get_allowed_languages(), equal_to(LANG_NAME_BY_ID))

    def test_statement(self):
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


class TestUtils__context_check_auth(TestCase):
    def setUp(self):
        super(TestUtils__context_check_auth, self).setUp()
        self.user = User()
        self.session.add(self.user)
        self.session.flush()

    def test_simple(self):
        self.request.session['user_id'] = self.user.id
        context = Context(self.request)
        context.check_auth()

    def test_moodle_session(self):
        with mock.patch('pynformatics.utils.context.RequestGetUserId', mock.Mock(return_value=self.user.id)):
            context = Context(self.request)
        context.check_auth()

    def test_no_user_id(self):
        context = Context(self.request)
        assert_that(
            calling(context.check_auth),
            raises(Unauthorized)
        )

    def test_bad_user_id(self):
        self.request.session['user_id'] = 'bad user id'
        context = Context(self.request)
        assert_that(
            calling(context.check_auth),
            raises(Unauthorized)
        )
