from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.run import Run
from pynformatics.testutils import TestCase


class TestModel__run_sync(TestCase):
    def setUp(self):
        super(TestModel__run_sync, self).setUp()

        self.create_problems()
        self.create_statements()
        self.create_users()

        self.ejudge_run = EjudgeRun(
            run_id=123,
            user=self.users[1],
            problem=self.problems[1],
            score=456,
        )
        self.session.add(self.ejudge_run)
        self.session.flush()

    def test_create(self):
        run = Run.sync(
            ejudge_run_id=self.ejudge_run.run_id,
            ejudge_contest_id=self.ejudge_run.contest_id,
        )
        self.session.flush()
        assert_that(run.user_id, equal_to(self.users[1].id))
        assert_that(run.problem_id, equal_to(self.problems[1].id))
        assert_that(run.score, equal_to(self.ejudge_run.score))
    
    def test_update(self):
        run = Run.sync(
            ejudge_run_id=self.ejudge_run.run_id,
            ejudge_contest_id=self.ejudge_run.contest_id,
        )
        run.statement = self.statements[0]
        self.ejudge_run.score = 179
        self.session.flush()

        assert_that(run.score, equal_to(456))
        assert_that(run.ejudge_score, equal_to(456))
        assert_that(run.statement_id, equal_to(self.statements[0].id))
        assert_that(self.ejudge_run.score, equal_to(179))

        run = Run.sync(
            ejudge_run_id=self.ejudge_run.run_id,
            ejudge_contest_id=self.ejudge_run.contest_id,
        )
        self.session.flush()
        assert_that(run.score, equal_to(179))
        assert_that(run.ejudge_score, equal_to(179))
        assert_that(run.statement_id, equal_to(self.statements[0].id))

        assert_that(self.session.query(Run).count(), equal_to(1))
