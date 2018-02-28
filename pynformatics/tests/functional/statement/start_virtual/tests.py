from hamcrest import (
    assert_that,
    has_entries,
    close_to,
)
import time

from pynformatics.model.course import Course
from pynformatics.model.user import User
from pynformatics.model.statement import Statement
from pynformatics.testutils import TestCase


class TestAPI__statement_start_virtual(TestCase):
    def setUp(self):
        super(TestAPI__statement_start_virtual, self).setUp()

        self.virtual_statement = Statement(
            virtual_olympiad=1,
            virtual_duration=300,
            time_start=0,
            time_stop=int(time.time()) + 100,
        )
        self.session.add(self.virtual_statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

    def test_simple(self):
        self.set_session({'user_id': self.user.id})
        response = self.app.post_json('/statement/1/start_virtual', {})
        assert_that(
            response.json,
            has_entries({
                'duration': self.virtual_statement.virtual_duration,
                'start': close_to(time.time(), 1),
            })
        )

    def test_with_password(self):
        password = 'secret'
        course = Course(password=password)
        self.session.add(course)
        self.virtual_statement.course = course

        self.set_session({'user_id': self.user.id})
        response = self.app.post_json(
            url='/statement/1/start_virtual',
            params={},
            status=403,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Password is wrong or missing',
            })
        )

        response = self.app.post_json(
            url='/statement/1/start_virtual',
            params={'password': 'wrong'},
            status=403,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Password is wrong or missing',
            })
        )

        self.app.post_json(
            url='/statement/1/start_virtual',
            params={'password': password},
        )
