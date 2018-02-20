import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.model.statement import Statement
from pynformatics.testutils import TestCase


class TestAPI__statement_standings(TestCase):
    def setUp(self):
        super(TestAPI__statement_standings, self).setUp()

        self.create_users()
        self.create_problems()

        self.statement = Statement()
        self.session.add(self.statement)
        self.session.flush()

    def send_request(self):
        response = self.app.get('/statement/1/standings')
        return response

    def test_simple(self):
        runs = [
            Run(
                run_id=1,
                contest_id=1,
                problem=self.problems[0],
                user=self.users[0],
                create_time=datetime.datetime(2018, 2, 23, 23, 3, 5),
                score=100,
                status=0,
            ),
        ]
        self.session.add_all(runs)

        pynformatics_runs = [
            PynformaticsRun(run=runs[0], statement_id=1)
        ]
        self.session.add_all(pynformatics_runs)

        response = self.send_request()
        assert_that(
            response.json,
            equal_to({
                '1': {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'runs': [
                        {
                            'run_id': 1,
                            'contest_id': 1,
                            'create_time': '2018-02-23T23:03:05',
                            'score': 100,
                            'status': 0,
                            'problem_id': 1,
                        }
                    ]
                }
            })
        )

    def test_does_not_creates_twice(self):
        # Ошибку кинет база данных при попытке создать объект с неуникальным ключом
        self.send_request()
        self.send_request()
