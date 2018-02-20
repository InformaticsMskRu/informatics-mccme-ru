import mock
from hamcrest import (
    assert_that,
    is_,
    contains_inanyorder,
)

from pynformatics.model.run import Run
from pynformatics.model.standings import ProblemStandings
from pynformatics.testutils import TestCase


class TestModel__problem_stadings_create(TestCase):
    def setUp(self):
        super(TestModel__problem_stadings_create, self).setUp()

        self.create_problems()
        self.create_users()

    def call_method(self,
                    problem_id=None,
                    ):
        problem_id = problem_id or self.problems[0].id
        update_mock = mock.Mock()
        with mock.patch.object(ProblemStandings, 'update', update_mock):
            result = ProblemStandings.create(problem_id=problem_id)

        return result, update_mock

    def test_simple(self):
        runs = [
            Run(
                run_id=1,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id
            ),
        ]
        self.session.add_all(runs)

        result, update_mock = self.call_method()
        from_db = self.session.query(ProblemStandings).one()

        assert_that(
            result,
            is_(from_db)
        )
        update_mock.assert_called_once_with(self.users[0])

    def test_ignores_other_problems(self):
        runs = [
            Run(
                run_id=1,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id
            ),
            Run(
                run_id=2,
                contest_id=self.problems[1].ejudge_contest_id,
                prob_id=self.problems[1].problem_id,
                user_id=self.users[0].ejudge_id
            ),
        ]
        self.session.add_all(runs)

        result, update_mock = self.call_method()
        from_db = self.session.query(ProblemStandings).one()

        assert_that(
            result,
            is_(from_db)
        )
        update_mock.assert_called_once_with(self.users[0])

    def test_two_users(self):
        runs = [
            Run(
                run_id=1,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[0].ejudge_id
            ),
            Run(
                run_id=2,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
                user_id=self.users[1].ejudge_id
            ),
        ]
        self.session.add_all(runs)

        result, update_mock = self.call_method()
        from_db = self.session.query(ProblemStandings).one()

        assert_that(
            result,
            is_(from_db)
        )

        update_mock_args = [call[0][0] for call in update_mock.call_args_list]
        assert_that(
            update_mock_args,
            contains_inanyorder(*self.users)
        )
