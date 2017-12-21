import time
import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)

from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import (
    StatementFinished,
    StatementNotStarted,
    StatementNotOlympiad,
)


class TestModel__statement_start(TestCase):
    def setUp(self):
        super(TestModel__statement_start, self).setUp()

        self.now = int(time.time())
        self.time_start = self.now - 60
        self.time_stop = self.now + 30

        self.statement = Statement(
            olympiad=1,
            time_start=self.time_start,
            time_stop=self.time_stop,
        )
        self.session.add(self.statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

    def test_simple(self):
        with mock.patch('pynformatics.model.statement.time.time', mock.Mock(return_value=self.now)), \
                mock.patch('pynformatics.model.statement.Statement.start_participant', mock.Mock()) as mock_start:
            self.statement.start(self.user)

        mock_start.assert_called_once_with(
            user=self.user,
            duration=self.time_stop - self.now,
        )

    def test_not_olympiad(self):
        statement = Statement(olympiad=0)
        self.session.add(statement)
        assert_that(
            calling(statement.start).with_args(self.user),
            raises(StatementNotOlympiad)
        )
