import time
from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)

from pynformatics.testutils import TestCase
from pynformatics.model.user import User
from pynformatics.model.statement import Statement
from pynformatics.model.participant import Participant


class TestAPI__statement_finish_virtual(TestCase):
    def setUp(self):
        super(TestAPI__statement_finish_virtual, self).setUp()

        self.virtual_statement = Statement(
            virtual_olympiad=1,
            virtual_duration=300,
        )
        self.session.add(self.virtual_statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

        self.actual_duration = 10
        self.participant = Participant(
            user_id=self.user.id,
            statement_id=self.virtual_statement.id,
            start=time.time() - self.actual_duration,
            duration=300,
        )
        self.session.add(self.participant)

    def test_simple(self):
        with self.mock_context_check_auth, \
                self.mock_context_user as mock_context_user:
            mock_context_user.return_value=self.user
            response = self.app.post('/statement/1/finish_virtual')
        assert_that(
            response.json,
            has_entries({
                'duration': close_to(self.actual_duration, 1),
                'start': self.participant.start,
            })
        )
