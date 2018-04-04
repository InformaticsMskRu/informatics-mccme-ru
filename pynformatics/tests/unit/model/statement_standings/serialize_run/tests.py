import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.standings import StatementStandings
from pynformatics.testutils import TestCase


class TestModel__statement_standings_serialize_run(TestCase):
    def setUp(self):
        super(TestModel__statement_standings_serialize_run, self).setUp()

        self.create_problems()

    def test_simple(self):
        run = EjudgeRun(
            run_id=1,
            contest_id=self.problems[1].ejudge_contest_id,
            prob_id=self.problems[1].problem_id,
            create_time=datetime.datetime(2018, 2, 24, 16, 44, 32),
            score=99,
            status=7,
        )
        self.session.add(run)
        self.session.flush()
        assert_that(
            StatementStandings.serialize_run(run),
            equal_to({
                'run_id': 1,
                'contest_id': 1,
                'create_time': '2018-02-24T16:44:32',
                'score': 99,
                'status': 7,
                'problem_id': 2,
            })
        )
