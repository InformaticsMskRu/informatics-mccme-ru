import datetime
from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)

from pynformatics.testutils import TestCase
from pynformatics.model.user import SimpleUser
from pynformatics.model.statement import Statement
from pynformatics.model.virtual_participant import VirtualParticipant


class TestAPI__statement_finish_virtual(TestCase):
    def setUp(self):
        super(TestAPI__statement_finish_virtual, self).setUp()

        self.virtual_statement = Statement(
            id=1,
            virtual_olympiad=1,
            virtual_duration=123,
        )
        self.session.add(self.virtual_statement)

        self.user = SimpleUser(id=1)
        self.session.add(self.user)

        self.duration = 10
        self.virtual_participant = VirtualParticipant(
            user_id=self.user.id,
            statement_id=self.virtual_statement.id,
            start=(datetime.datetime.now() - datetime.timedelta(minutes=self.duration)).timestamp(),
            duration=20,
        )
        self.session.add(self.virtual_participant)

    def test_simple(self):
        with self.mock_context_check_auth, \
                self.mock_context_user as mock_context_user:
            mock_context_user.return_value=self.user
            response = self.app.post('/statement/1/finish_virtual')
        assert_that(
            response.json,
            has_entries({
                'duration': close_to(self.duration, 1),
                'start': self.virtual_participant.start,
            })
        )
