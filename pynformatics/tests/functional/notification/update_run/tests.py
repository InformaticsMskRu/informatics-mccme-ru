from hamcrest import (
    assert_that,
    contains_inanyorder,
    equal_to,
    has_entries,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.run import Run
from pynformatics.testutils import TestCase
from pynformatics.utils.notify import Client


class TestAPI__notification_update_run(TestCase):
    def setUp(self):
        super(TestAPI__notification_update_run, self).setUp()

        self.create_problems()
        self.create_users()

        self.ej_run = EjudgeRun(
            run_id=123,
            user=self.users[0],
            problem=self.problems[0],
        )
        self.session.add(self.ej_run)
        self.session.flush()

        self.run = Run.from_ejudge_run(self.ej_run)
        self.session.add(self.run)
        self.session.flush()
    
    def send_request(self, contest_id, run_id, status=200):
        response = self.app.get(
            f'/notification/update_run?contest_id={contest_id}&run_id={run_id}',
            status=status,
        )
        return response

    def test_sync(self):
        self.ej_run.status = 121
        self.send_request(
            contest_id=self.ej_run.contest_id,
            run_id=self.ej_run.run_id,
        )

        assert_that(self.run.status, equal_to(121))
    
    def test_notify(self):
        author_client = Client(user_id=self.users[0].id)
        other_client = Client(user_id=self.users[1].id)

        self.ej_run.status = 121
        self.send_request(
            contest_id=self.ej_run.contest_id,
            run_id=self.ej_run.run_id,
        )

        assert_that(
            author_client.get_message(),
            has_entries({
                'runs': contains_inanyorder(
                    has_entries({
                        'id': self.run.id,
                        'problem_id': self.problems[0].id,
                        'statement_id': None,
                        'score': None,
                        'status': 121,
                        'language_id': None,
                        'create_time': 'None',
                    })
                )
            })
        )
        assert_that(
            other_client.get_message(),
            equal_to(None),
        )

    def test_run_not_found(self):
        response = self.send_request(contest_id=11, run_id=22, status=404)
        assert_that(
            response.json,
            equal_to({
                'code': 404,
                'message': 'Run not found',
            })
        )
