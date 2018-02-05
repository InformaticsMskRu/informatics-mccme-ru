import mock
import time
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)

from pynformatics.model.participant import Participant
from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import (
    StatementCanOnlyStartOnce,
    StatementFinished,
    StatementNotStarted,
    StatementOnlyOneOngoing,
)


class TestModel__statement_start_participant(TestCase):
    def setUp(self):
        super(TestModel__statement_start_participant, self).setUp()

        self.now = int(time.time())
        self.duration = 10

        self.user = User()
        self.session.add(self.user)

        self.time_start = self.now
        self.time_stop = self.now + 100
        self.statement = Statement(
            time_start=self.time_start,
            time_stop=self.time_stop,
        )
        self.session.add(self.statement)

        self.session.flush()

    def test_simple(self):
        with mock.patch('pynformatics.model.statement.time.time', mock.Mock(return_value=self.now)):
            participant = self.statement.start_participant(
                user=self.user,
                duration=self.duration,
            )
        assert_that(
            participant.user_id,
            equal_to(self.user.id)
        )
        assert_that(
            participant.statement_id,
            equal_to(self.statement.id)
        )
        assert_that(
            participant.start,
            equal_to(self.now)
        )
        assert_that(
            participant.duration,
            equal_to(self.duration)
        )
        self.session.query(Participant).filter(
            Participant.user_id == self.user.id
        ).filter(
            Participant.statement_id == self.statement.id
        ).filter(
            Participant.start == self.now
        ).filter(
            Participant.duration == self.duration
        ).one()

    def test_can_only_start_once(self):
        participant = Participant(
            user_id=self.user.id,
            statement_id=self.statement.id,
            start=self.now - self.duration,
            duration = self.duration,
        )
        self.session.add(participant)
        assert_that(
            calling(self.statement.start_participant).with_args(
                user=self.user,
                duration=self.duration,
            ),
            raises(StatementCanOnlyStartOnce)
        )

    def test_only_one_ongoing(self):
        participant = Participant(
            user_id=self.user.id,
            statement_id=self.statement.id + 1,
            start=self.now - self.duration,
            duration=self.duration * 2,
        )
        self.session.add(participant)
        assert_that(
            calling(self.statement.start_participant).with_args(
                user=self.user,
                duration=self.duration,
            ),
            raises(StatementOnlyOneOngoing)
        )
