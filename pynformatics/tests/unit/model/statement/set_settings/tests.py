import time
from hamcrest import (
    assert_that,
    calling,
    close_to,
    equal_to,
    raises,
)

from pynformatics.testutils import TestCase
from pynformatics.model.statement import Statement
from pynformatics.utils.exceptions import StatementSettingsValidationError


class TestModel__statement_set_settings(TestCase):
    def setUp(self):
        super(TestModel__statement_set_settings, self).setUp()

        self.statement = Statement()
        self.session.add(self.statement)

    def test_simple(self):
        settings = {
            'allowed_languages': [1],
        }
        self.statement.set_settings(settings)
        assert_that(
            self.statement.settings,
            equal_to(settings),
        )
        assert_that(
            self.statement.time_modified,
            close_to(time.time(), 1),
        )

    def test_type_olympiad(self):
        self.statement.set_settings({
            'type': 'olympiad',
        })
        assert_that(
            self.statement.olympiad,
            equal_to(True)
        )
        assert_that(
            self.statement.virtual_olympiad,
            equal_to(False)
        )

    def test_type_virtual(self):
        self.statement.set_settings({
            'type': 'virtual',
        })
        assert_that(
            self.statement.olympiad,
            equal_to(False)
        )
        assert_that(
            self.statement.virtual_olympiad,
            equal_to(True)
        )

    def test_type_null(self):
        self.statement.set_settings({
            'type': None,
        })
        assert_that(
            self.statement.olympiad,
            equal_to(False)
        )
        assert_that(
            self.statement.virtual_olympiad,
            equal_to(False)
        )

    def test_time_start_stop(self):
        time_start = 123
        time_stop = 456
        self.statement.set_settings({
            'time_start': time_start,
            'time_stop': time_stop,
        })
        assert_that(
            self.statement.time_start,
            equal_to(time_start)
        )
        assert_that(
            self.statement.time_stop,
            equal_to(time_stop)
        )

    def test_additional_property(self):
        settings = {
            'additional_propery': True,
        }
        assert_that(
            calling(self.statement.set_settings).with_args(settings),
            raises(StatementSettingsValidationError),
        )
