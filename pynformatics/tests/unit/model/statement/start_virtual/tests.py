import time
import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    is_not,
    raises,
)

from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import (
    StatementNotStarted,
    StatementNotVirtual,
)



class TestModel__Statement_start_virtual(TestCase):
    def setUp(self):
        super(TestModel__Statement_start_virtual, self).setUp()

        self.now = int(time.time())
        self.virtual_duration = 60
        self.time_start = self.now - 60

        self.statement = Statement(
            virtual_olympiad=1,
            virtual_duration=self.virtual_duration,
            time_start=self.time_start,
        )
        self.session.add(self.statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

    def test_simple(self):
        with mock.patch('pynformatics.model.statement.time.time', mock.Mock(return_value=self.now)), \
                mock.patch('pynformatics.model.statement.Statement.start_participant', mock.Mock()) as mock_start:
            self.statement.start_virtual(self.user)
        mock_start.assert_called_once_with(
            user=self.user,
            duration=self.virtual_duration,
        )

    def test_not_virtual(self):
        statement = Statement(virtual_olympiad=0)
        self.session.add(statement)
        assert_that(
            calling(statement.start_virtual).with_args(self.user),
            raises(StatementNotVirtual)
        )

    def test_ignores_not_started(self):
        # Виртуальные контесты должны игнорировать поля time_start, time_end для согласования с
        # поведением на старом информатиксе
        with mock.patch('pynformatics.model.statement.time.time', mock.Mock(return_value=self.time_start - 1)):
            assert_that(
                calling(self.statement.start_virtual).with_args(self.user),
                is_not(raises(StatementNotStarted)),
            )
