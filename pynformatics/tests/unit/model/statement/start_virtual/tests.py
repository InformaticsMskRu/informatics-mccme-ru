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
    StatementNotVirtual,
    StatementOnlyOneOngoingVirtual,
    StatementVirtualCanOnlyStartOnce,
)


class TestModel__Statement_start_virtual(TestCase):
    def setUp(self):
        super(TestModel__Statement_start_virtual, self).setUp()

        self.virtual_statement = Statement(
            name='test virtual statement',
            virtual_olympiad=1,
            virtual_duration=123,
        )
        self.session.add(self.virtual_statement)

        self.virtual_statement2 = Statement(
            name='test virtual statement 2',
            virtual_olympiad=1,
            virtual_duration=234,
        )
        self.session.add(self.virtual_statement2)

        self.statement = Statement(
            name='test statement',
        )
        self.session.add(self.statement)

        self.user = SimpleUser(
            firstname='test user'
        )
        self.session.add(self.user)

    def test_simple(self):
        """
        Запускает виртуальный контест для пользователя
        """
        virtual_participant = self.virtual_statement.start_virtual(self.user)
        db_virtual_participant = self.session.query(VirtualParticipant).filter(
            VirtualParticipant.user_id == self.user.id).filter(
            VirtualParticipant.statement_id == self.virtual_statement.id
        ).one()

        assert_that(
            virtual_participant.start,
            close_to(int(time.time()), 1)
        )
        assert_that(
            virtual_participant.duration,
            equal_to(self.virtual_statement.virtual_duration)
        )
        assert_that(
            virtual_participant.start,
            equal_to(db_virtual_participant.start)
        )
        assert_that(
            virtual_participant.duration,
            equal_to(db_virtual_participant.duration)
        )

    def test_not_virtual(self):
        assert_that(
            calling(self.statement.start_virtual).with_args(self.user),
            raises(StatementNotVirtual)
        )

    def test_can_only_start_once(self):
        self.virtual_statement.start_virtual(self.user)
        assert_that(
            calling(self.virtual_statement.start_virtual).with_args(self.user),
            raises(StatementVirtualCanOnlyStartOnce)
        )

    def test_only_one_ongoing_virtual(self):
        """
        Начинает контест для пользователя и пытается начать другой контест
        """
        self.virtual_statement2.start_virtual(self.user)
        assert_that(
            calling(self.virtual_statement.start_virtual).with_args(self.user),
            raises(StatementOnlyOneOngoingVirtual)
        )
