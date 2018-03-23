import mock
from hamcrest import (
    assert_that,
    has_entries,
    has_key,
    is_not,
)

from pynformatics.testutils import TestCase
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.user import SimpleUser


class TestModel__run_serialize(TestCase):
    def setUp(self):
        super(TestModel__run_serialize, self).setUp()

        self.create_problems()

        self.author = SimpleUser(
            ejudge_id=1,
            firstname='author_firstname',
            lastname='author_lastname',
        )
        self.other = SimpleUser(
            ejudge_id=2,
            firstname='other_firstname',
            lastname='other_lastname',
        )
        self.session.add_all([self.author, self.other])
        self.session.flush()

        self.run = EjudgeRun(
            user=self.author,
            run_id=123,
            problem=self.problems[0],
        )
        self.session.add(self.run)
        self.session.flush([self.run])

        self.context_mock = mock.Mock()

        self.pynformatics_run_serialized = {
            'some_key': 'some_value',
        }
        self.pynformatics_run_mock = mock.Mock()
        self.pynformatics_run_mock.serialize = mock.Mock(return_value=self.pynformatics_run_serialized)

    def call_serialize(self):
        with mock.patch(
                'pynformatics.model.ejudge_run.EjudgeRun.get_pynformatics_run',
                mock.Mock(return_value=self.pynformatics_run_mock)
        ):
            return self.run.serialize(self.context_mock)

    def test_for_author(self):
        self.context_mock.user = self.author
        result = self.call_serialize()
        assert_that(
            result,
            has_entries({
                'status': None,
                'contest_id': self.run.contest_id,
                'prob_id': 1,
                'run_id': self.run.run_id,
                'create_time': 'None',
                'lang_id': None,
                'score': None,
                'size': None,
            })
        )
        assert_that(
            result,
            has_entries(self.pynformatics_run_serialized)
        )
        assert_that(
            result,
            is_not(has_key('user'))
        )

    def test_for_other(self):
        self.context_mock.user = self.other
        result = self.call_serialize()
        assert_that(
            result,
            has_entries({
                'status': None,
                'contest_id': self.run.contest_id,
                'prob_id': 1,
                'run_id': self.run.run_id,
                'create_time': 'None',
                'lang_id': None,
                'score': None,
                'size': None,
                'user': self.author.serialize(mock.Mock())
            })
        )
