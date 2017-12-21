import time
import mock

from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestModel__statement_finish(TestCase):
    def setUp(self):
        super(TestModel__statement_finish, self).setUp()

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
        with mock.patch('pynformatics.model.statement.Statement.finish_participant', mock.Mock()) as mock_finish:
            self.statement.finish(self.user)
        mock_finish.assert_called_once_with(self.user)
