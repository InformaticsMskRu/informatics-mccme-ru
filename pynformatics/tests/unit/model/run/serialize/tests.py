import datetime
import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.run import Run
from pynformatics.testutils import TestCase


class TestModel__run_serialize(TestCase):
    def setUp(self):
        super(TestModel__run_serialize, self).setUp()

        self.create_problems()
        self.create_statements()
        self.create_users()
    
    def test_simple(self):
        run = Run(
            user=self.users[0],
            problem=self.problems[0],
            statement=self.statements[0],
            score=123,
            create_time=datetime.datetime(2018, 3, 24, 10, 49, 0),
            ejudge_score=456,
            ejudge_status=7,
            ejudge_language_id=27,
            ejudge_create_time=datetime.datetime(2010, 1, 1, 1, 1, 1)
        )
        self.session.add(run)
        self.session.flush()

        assert_that(
            run.serialize(mock.Mock()),
            equal_to({
                'id': 1,
                'problem_id': self.problems[0].id,
                'statement_id': self.statements[0].id,
                'score': 123,
                'status': 7,
                'language_id': 27,
                'create_time': '2018-03-24 10:49:00',
            })
        )
