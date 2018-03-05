import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.run import Run
from pynformatics.model.standings import StatementStandings
from pynformatics.testutils import TestCase


class TestModel__statement_standings_update(TestCase):
    def setUp(self):
        super(TestModel__statement_standings_update, self).setUp()

        self.create_problems()
        self.create_statements()
        self.create_users()

        self.standings = StatementStandings(
            statement_id=self.statements[0].id
        )
        self.run = Run(
            run_id=1,
            problem=self.problems[0],
            user=self.users[0],
            create_time=datetime.datetime(2018, 2, 24, 11, 47, 23),
            score=100,
            status=0,
        )

        self.runs = [
            Run(
                run_id=2,
                problem=self.problems[0],
                user=self.users[0],
                create_time=datetime.datetime(2018, 2, 24, 12, 0, 0)
            ),
            Run(
                run_id=3,
                problem=self.problems[0],
                user=self.users[0],
                create_time=datetime.datetime(2018, 2, 24, 13, 0, 0)
            ),
            Run(
                run_id=4,
                problem=self.problems[0],
                user=self.users[0],
                create_time=datetime.datetime(2018, 2, 24, 14, 0, 0)
            ),
        ]

        self.session.add_all((self.standings, self.run, *self.runs))
        self.session.flush()

    def test_update_empty(self):
        self.standings.update(self.run)
        assert_that(
            self.standings.json,
            equal_to({
                '1': {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'runs': [
                        {
                            'run_id': 1,
                            'contest_id': 1,
                            'problem_id': 1,
                            'score': 100,
                            'status': 0,
                            'create_time': '2018-02-24T11:47:23',
                        }
                    ]
                }
            })
        )

    def test_insert_last(self):
        self.session.add_all(self.runs)
        for run in self.runs:
            self.standings.update(run)

        json_runs = self.standings.json['1']['runs']
        assert_that(
            [json_run['run_id'] for json_run in json_runs],
            equal_to([2, 3, 4])
        )

    def test_insert_first(self):
        for run in self.runs[::-1]:
            self.standings.update(run)

        json_runs = self.standings.json['1']['runs']
        assert_that(
            [json_run['run_id'] for json_run in json_runs],
            equal_to([2, 3, 4])
        )

    def test_insert_middle(self):
        self.runs[1], self.runs[2] = self.runs[2], self.runs[1]
        for run in self.runs:
            self.standings.update(run)

        json_runs = self.standings.json['1']['runs']
        assert_that(
            [json_run['run_id'] for json_run in json_runs],
            equal_to([2, 3, 4])
        )

    def test_replace(self):
        for run in self.runs:
            self.standings.update(run)

        self.runs[0].score = 100
        self.standings.update(self.runs[0])

        json_runs = self.standings.json['1']['runs']
        assert_that(
            [json_run['run_id'] for json_run in json_runs],
            equal_to([2, 3, 4])
        )
        assert_that(
            json_runs[0]['score'],
            equal_to(100)
        )
