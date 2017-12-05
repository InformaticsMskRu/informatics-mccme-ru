import mock
import time
from hamcrest import (
    assert_that,
    calling,
    close_to,
    equal_to,
    raises,
)

from pynformatics.model.participant import Participant
from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import (
    StatementNothingToFinish,
)


class TestModel__statement_finish_participant(TestCase):
    def setUp(self):
        super(TestModel__statement_finish_participant, self).setUp()

        self.now = int(time.time())
        self.duration = 10

        self.user = User()
        self.session.add(self.user)

        self.statement = Statement()
        self.session.add(self.statement)

        self.session.flush()

    def test_simple(self):
        participant = Participant(
            user_id=self.user.id,
            statement_id=self.statement.id,
            start=self.now - self.duration,
            duration = self.duration * 2,
        )
        self.session.add(participant)
        finished = self.statement.finish_participant(self.user)
        assert_that(
            finished.user_id,
            equal_to(self.user.id)
        )
        assert_that(
            finished.statement_id,
            equal_to(self.statement.id)
        )
        assert_that(
            finished.start,
            equal_to(self.now - self.duration)
        )
        assert_that(
            finished.duration,
            close_to(self.duration, 2)
        )

        db_participant = self.session.query(Participant).filter(
            Participant.user_id == self.user.id
        ).filter(
            Participant.statement_id == self.statement.id
        ).filter(
            Participant.start == self.now - self.duration
        ).one()
        assert_that(
            db_participant.duration,
            equal_to(finished.duration)
        )

    def test_no_active_participant(self):
        assert_that(
            calling(self.statement.finish_participant).with_args(self.user),
            raises(StatementNothingToFinish)
        )

    def test_active_participant_for_other_statement(self):
        participant = Participant(
            user_id=self.user.id,
            statement_id=self.statement.id + 1,
            start=self.now - self.duration,
            duration=self.duration * 2,
        )
        self.session.add(participant)
        assert_that(
            calling(self.statement.finish_participant).with_args(self.user),
            raises(StatementNothingToFinish)
        )
