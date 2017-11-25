from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)
import time

from pynformatics.testutils import TestCase
from pynformatics.model.user import SimpleUser
from pynformatics.model.statement import Statement


class TestAPI__Statement_start_virtual(TestCase):
    def setUp(self):
        super(TestAPI__Statement_start_virtual, self).setUp()

        self.virtual_statement = Statement(
            id=1,
            virtual_olympiad=1,
            virtual_duration=123,
        )
        self.session.add(self.virtual_statement)

        self.user = SimpleUser(id=1)
        self.session.add(self.user)

    def test_simple(self):
        with self.mock_context_check_auth, \
                self.mock_context_user as mock_context_user:
            mock_context_user.return_value=self.user
            response = self.app.post('/statement/1/start_virtual')
        assert_that(
            response.json,
            has_entries({
                'duration': self.virtual_statement.virtual_duration,
                'start': close_to(time.time(), 1),
            })
        )
