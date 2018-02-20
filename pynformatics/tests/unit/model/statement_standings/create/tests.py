import datetime
import mock

from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.model.standings import StatementStandings
from pynformatics.testutils import TestCase


class TestModel__statement_standings_create(TestCase):
    def setUp(self):
        super(TestModel__statement_standings_create, self).setUp()

        self.create_problems()
        self.create_statements()
        self.create_users()

    def call_method(self,
                    statement_id=None,
                    ):
        statement_id = statement_id or self.statements[0].id

        update_mock = mock.Mock()
        with mock.patch.object(StatementStandings, 'update', update_mock):
            standings = StatementStandings.create(statement_id=statement_id)

        return standings, update_mock

    def test_simple(self):
        statement_ids = [
            self.statements[0].id,
            self.statements[1].id,
        ]
        runs = [
            Run(
                run_id=1,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
                create_time=datetime.datetime(2018, 2, 24, 16, 36, 0)
            ),
            Run(
                run_id=2,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
                create_time=datetime.datetime(2018, 2, 24, 16, 36, 0)
            )
        ]
        pynformatics_runs = [
            PynformaticsRun(
                run=run,
                statement_id=statement_id,
            )
            for run, statement_id in zip(runs, statement_ids)
        ]
        self.session.add_all(runs)
        self.session.add_all(pynformatics_runs)
        self.session.flush()

        standings, update_mock = self.call_method()
        update_mock.assert_called_once_with(runs[0])
