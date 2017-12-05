import time
import mock

from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestModel__statement_finish(TestCase):
    def setUp(self):
        super(TestModel__statement_finish, self).setUp()

        self.now = int(time.time())
        self.timestart = self.now - 60
        self.timestop = self.now + 30

        self.statement = Statement(
            olympiad=1,
            timestart=self.timestart,
            timestop=self.timestop,
        )
        self.session.add(self.statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

    def test_simple(self):
        with mock.patch('pynformatics.model.statement.Statement.finish_participant', mock.Mock()) as mock_finish:
            self.statement.finish(self.user)
        mock_finish.assert_called_once_with(self.user)
