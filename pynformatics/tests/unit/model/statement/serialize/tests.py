from hamcrest import (
    assert_that,
    has_entries,
    has_items,
    is_not,
)
import mock

from pynformatics.model.course_module import CourseModule
from pynformatics.model.participant import Participant
from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestModel__statement_serialize(TestCase):
    def setUp(self):
        super(TestModel__statement_serialize, self).setUp()

        self.statement = Statement()
        self.session.add(self.statement)

        self.user = User()
        self.session.add(self.user)

        self.session.flush()

        self.course_model = CourseModule(
            instance=self.statement.id,
            module=19,
        )
        self.session.add(self.course_model)

        self.participant = Participant(
            user_id=self.user.id,
            statement_id=self.statement.id,
        )
        self.session.add(self.participant)

        self.mock_context = mock.Mock()


    def test_simple(self):
        assert_that(
            self.statement.serialize(self.mock_context),
            has_entries({
                'course': None,
                'course_module_id': 1,
                'id': self.statement.id,
                'name': None,
                'olympiad': None,
                'problems': {},
                'settings': None,
                'time_start': None,
                'time_stop': None,
                'virtual_duration': None,
                'virtual_olympiad': None,
            })
        )

    def test_olympiad(self):
        self.statement.olympiad = True
        self.mock_context.user = None
        assert_that(
            self.statement.serialize(self.mock_context),
            is_not(has_items('problems'))
        )
        self.mock_context.user = self.user
        self.mock_context.user_id = self.user.id
        assert_that(
            self.statement.serialize(self.mock_context),
            has_items('problems')
        )

    def test_virtual_olympiad(self):
        self.statement.virtual_olympiad = True
        self.mock_context.user = None
        assert_that(
            self.statement.serialize(self.mock_context),
            is_not(has_items('problems'))
        )
        self.mock_context.user = self.user
        self.mock_context.user_id = self.user.id
        assert_that(
            self.statement.serialize(self.mock_context),
            has_items('problems')
        )
