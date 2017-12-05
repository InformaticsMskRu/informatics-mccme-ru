import time
from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)

from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestAPI__statement_start(TestCase):
    def setUp(self):
        super(TestAPI__statement_start, self).setUp()

        self.user = User()
        self.session.add(self.user)

        self.now = time.time()
        self.duration = 290
        self.statement = Statement(
            olympiad=1,
            timestart=self.now - 10,
            timestop=self.now + self.duration,
        )
        self.session.add(self.statement)

        self.session.flush()

    def test_simple(self):
        with self.mock_context_user as mock_context_user, \
                self.mock_context_check_auth:
            mock_context_user.return_value = self.user
            response = self.app.post('/statement/%s/start' % self.statement.id, {})
        assert_that(
            response.json,
            has_entries({
                'statement_id': self.statement.id,
                'start': close_to(self.now, 1),
                'duration': close_to(self.duration, 1),
            })
        )
