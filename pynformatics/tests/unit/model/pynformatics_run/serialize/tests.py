import mock
from hamcrest import (
    assert_that,
    is_not,
    has_entries,
    has_key,
)

from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.model.user import SimpleUser
from pynformatics.testutils import TestCase


class TestModel__pynformatics_run__serialize(TestCase):
    def setUp(self):
        super(TestModel__pynformatics_run__serialize, self).setUp()

        self.author = SimpleUser(ejudge_id=666)
        self.other = SimpleUser(ejudge_id=777)
        self.run = Run(
            run_id=1,
            contest_id=2,
            user=self.author,
        )
        self.pynformatics_run = PynformaticsRun(
            run=self.run,
            statement_id=123,
            source='some source',
        )

        self.session.add_all([
            self.author,
            self.other,
            self.run,
            self.pynformatics_run
        ])
        self.session.flush()

        self.context_mock = mock.Mock()

    def test_for_author(self):
        self.context_mock.user = self.author
        result = self.pynformatics_run.serialize(self.context_mock)
        assert_that(
            result,
            has_entries({
                'statement_id': self.pynformatics_run.statement_id,
                'source': self.pynformatics_run.source,
            })
        )

    def test_for_other(self):
        self.context_mock.user = self.other
        result = self.pynformatics_run.serialize(self.context_mock)
        assert_that(
            result,
            has_entries({
                'statement_id': self.pynformatics_run.statement_id,
            })
        )
        assert_that(
            result,
            is_not(has_key('source'))
        )
