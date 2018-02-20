import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.run import Run
from pynformatics.model.standings import ProblemStandings
from pynformatics.testutils import TestCase


class TestModel__problem_standings_update(TestCase):
    def setUp(self):
        super(TestModel__problem_standings_update, self).setUp()

        self.create_problems()
        self.create_users()

        self.standings = ProblemStandings(problem_id=self.problems[0].id)
        self.session.add(self.standings)
        self.session.flush()

    def test_ignores_after_ok(self):
        runs = [
            Run(
                run_id=1,
                score=100,
                status=0,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
            ),
            Run(
                run_id=2,
                score=10,
                status=7,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
            )
        ]
        self.session.add_all(runs)

        self.standings.update(self.users[0])
        assert_that(
            self.standings.json,
            equal_to({
                1: {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 1,
                    'score': 100,
                    'status': 0,
                }
            })
        )

    def test_orders_by_time(self):
        runs = [
            Run(
                run_id=1,
                score=100,
                status=0,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
                create_time=datetime.datetime(2018, 2, 22, 20, 39, 0)
            ),
            Run(
                run_id=2,
                score=10,
                status=7,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
                create_time=datetime.datetime(2018, 2, 22, 20, 35, 0)
            )
        ]
        self.session.add_all(runs)

        self.standings.update(self.users[0])
        assert_that(
            self.standings.json,
            equal_to({
                1: {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 2,
                    'score': 100,
                    'status': 0,
                }
            })
        )

    def test_maximum(self):
        runs = [
            Run(
                run_id=7,
                score=30,
                status=0,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
            ),
            Run(
                run_id=2,
                score=40,
                status=7,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
            ),
            Run(
                run_id=3,
                score=25,
                status=7,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id,
            )
        ]
        self.session.add_all(runs)

        self.standings.update(self.users[0])
        assert_that(
            self.standings.json,
            equal_to({
                1: {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 3,
                    'score': 40,
                    'status': 7,
                }
            })
        )

    def test_no_runs(self):
        self.standings.update(self.users[0])
        assert_that(
            self.standings.json,
            equal_to({
                1: {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 0,
                    'score': 0,
                    'status': None,
                }
            })
        )


