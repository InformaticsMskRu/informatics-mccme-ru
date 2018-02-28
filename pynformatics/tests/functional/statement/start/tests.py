import time
from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)

from pynformatics.model.course import Course
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
            time_start=self.now - 10,
            time_stop=self.now + self.duration,
        )
        self.session.add(self.statement)

        self.session.flush()

    def test_simple(self):
        self.set_session({'user_id': self.user.id})
        response = self.app.post_json('/statement/%s/start' % self.statement.id, {})
        assert_that(
            response.json,
            has_entries({
                'statement_id': self.statement.id,
                'start': close_to(self.now, 1),
                'duration': close_to(self.duration, 1),
            })
        )

    def test_with_password(self):
        password = 'secret'
        course = Course(password=password)
        self.session.add(course)
        self.statement.course = course

        self.set_session({'user_id': self.user.id})
        response = self.app.post_json(
            url='/statement/%s/start' % self.statement.id,
            params={},
            status=403
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Password is wrong or missing'
            })
        )

        response = self.app.post_json(
            url='/statement/%s/start' % self.statement.id,
            params={'password': 'wrong'},
            status=403
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Password is wrong or missing'
            })
        )

        self.app.post_json(
            url='/statement/%s/start' % self.statement.id,
            params={'password': password},
        )
