import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.pynformatics_run import PynformaticsRun


class TestModel__run_get_pynformatics_run(TestCase):
    def setUp(self):
        super(TestModel__run_get_pynformatics_run, self).setUp()
        self.run_id = 123
        self.contest_id = 456
        self.run = EjudgeRun(
            run_id=self.run_id,
            contest_id=self.contest_id
        )

        self.session.add(self.run)
        self.session.flush()


    def test_creates_if_none(self):
        sources = 'some sources'
        get_sources_mock = mock.Mock(return_value=sources)
        with mock.patch('pynformatics.model.ejudge_run.EjudgeRun.get_sources', get_sources_mock):
            pynformatics_run = self.run.get_pynformatics_run()

        get_sources_mock.assert_called_once()
        assert_that(
            pynformatics_run.statement_id,
            equal_to(None)
        )
        assert_that(
            pynformatics_run.source,
            equal_to(sources)
        )
        assert_that(
            len(self.session.query(PynformaticsRun).all()),
            equal_to(1),
        )

    def test_gets_if_exists(self):
        statement_id = 123
        source = 'some source'
        pynformatics_run = PynformaticsRun(
            run_id=self.run_id,
            contest_id=self.contest_id,
            statement_id=statement_id,
            source=source,
        )
        self.session.add(pynformatics_run)

        fetched_pynformatics_run = self.run.get_pynformatics_run()
        assert_that(
            fetched_pynformatics_run.statement_id,
            equal_to(statement_id)
        )
        assert_that(
            fetched_pynformatics_run.source,
            equal_to(source),
        )

