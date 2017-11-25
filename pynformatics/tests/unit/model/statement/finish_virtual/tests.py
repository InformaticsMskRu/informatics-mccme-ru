import datetime
import mock
import time
from hamcrest import (
    assert_that,
    equal_to,
    close_to,
    calling,
    raises,
)

from pynformatics.testutils import TestCase
from pynformatics.model.statement import Statement
from pynformatics.model.user import SimpleUser
from pynformatics.model.virtual_participant import VirtualParticipant
from pynformatics.utils.exceptions import (
    StatementNothingToFinish,
)


class TestModel__Statement_start_virtual(TestCase):
    def setUp(self):
        super(TestModel__Statement_start_virtual, self).setUp()

        self.virtual_statement = Statement(
            id=1,
            name='test virtual statement',
            virtual_olympiad=1,
            virtual_duration=123,
        )
        self.session.add(self.virtual_statement)

        self.user = SimpleUser(
            id=1,
            firstname='test user',
        )
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
        virtual_participant = self.virtual_statement.finish_virtual(self.user)
        db_virtual_participant = self.session.query(VirtualParticipant).filter(
            VirtualParticipant.user_id == self.user.id
        ).filter(
            VirtualParticipant.statement_id == self.virtual_statement.id
        ).one()

        assert_that(
            virtual_participant.duration,
            close_to(self.duration, 1)
        )
        assert_that(
            virtual_participant.duration,
            equal_to(db_virtual_participant.duration)
        )

    def test_finish_twice(self):
        self.virtual_statement.finish_virtual(self.user)
        assert_that(
            calling(self.virtual_statement.finish_virtual).with_args(self.user),
            raises(StatementNothingToFinish)
        )
