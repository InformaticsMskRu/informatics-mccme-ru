import datetime
from hamcrest import (
    assert_that,
    has_entries,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.run import Run
from pynformatics.testutils import TestCase
from pynformatics.utils.functions import attrs_to_dict


class TestModel__run_from_ejudge_run(TestCase):
    def setUp(self):
        super(TestModel__run_from_ejudge_run, self).setUp()

        self.create_problems()
        self.create_users()

    def test_simple(self):
        ejudge_run = EjudgeRun(
            run_id=2,
            user=self.users[0],
            problem=self.problems[0],
            run_uuid='some string',
            score=10,
            status=7,
            lang_id=27,
            test_num=3,
            create_time=datetime.datetime(2018, 3, 24, 9, 51, 30),
            last_change_time=datetime.datetime(2018, 3, 24, 9, 51, 31),
        )
        self.session.add(ejudge_run)
        self.session.flush()

        run = Run.from_ejudge_run(ejudge_run)
        self.session.add(run)
        self.session.flush()

        assert_that(
            attrs_to_dict(
                run,
                'user_id',
                'problem_id',
                'statement_id',
                'score',
                'ejudge_run_id',
                'ejudge_contest_id',
                'ejudge_score',
                'ejudge_status',
                'ejudge_language_id',
                'ejudge_test_num',
                'ejudge_create_time',
                'ejudge_last_change_time',
            ),
            has_entries({
                'user_id': self.users[0].id,
                'problem_id': self.problems[0].id,
                'score': ejudge_run.score,
                'ejudge_run_id': ejudge_run.run_id,
                'ejudge_contest_id': ejudge_run.contest_id,
                'ejudge_score': ejudge_run.score,
                'ejudge_status': ejudge_run.status,
                'ejudge_language_id': ejudge_run.lang_id,
                'ejudge_test_num': ejudge_run.test_num,
                'ejudge_create_time': ejudge_run.create_time,
                'ejudge_last_change_time': ejudge_run.last_change_time,
            })
        )
