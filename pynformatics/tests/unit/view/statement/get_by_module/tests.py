import mock
from hamcrest import (
    assert_that,
    has_entries,
)

from pynformatics.model.course_module import CourseModule
from pynformatics.model.statement import Statement
from pynformatics.testutils import TestCase
from pynformatics.view.statement import statement_get_by_module


class TestView__statement_get_by_module(TestCase):
    def setUp(self):
        super(TestView__statement_get_by_module, self).setUp()

        self.statement = Statement()
        self.session.add(self.statement)
        self.session.flush()

        self.course_module = CourseModule(
            id=123,
            instance=self.statement.id,
            module=19,
        )
        self.session.add(self.course_module)
        self.session.flush()

    def test_simple(self):
        self.request.params = {'course_module_id': self.course_module.id}
        with mock.patch('pynformatics.view.statement.statement_get', mock.Mock()) as statement_get_mock:
            statement_get_by_module(self.request)
            statement_get_mock.assert_called_once()
            assert_that(
                statement_get_mock.call_args_list[0][0][0].matchdict,
                has_entries({
                    'statement_id': self.statement.id,
                })
            )
