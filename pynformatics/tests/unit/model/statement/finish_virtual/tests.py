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


class TestModel__Statement_start_virtual(TestCase):
    def setUp(self):
        super(TestModel__Statement_start_virtual, self).setUp()

        self.now = int(time.time())
        self.virtual_duration = 100
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
        with mock.patch('pynformatics.model.statement.Statement.finish_participant', mock.Mock()) as mock_finish:
            self.statement.finish_virtual(self.user)
        mock_finish.assert_called_once_with(self.user)
