import mock
from hamcrest import (
    assert_that,
    contains_inanyorder
)

from pynformatics.model.problem import EjudgeProblem, Problem
from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.model.statement import Statement
from pynformatics.model.user import SimpleUser
from pynformatics.testutils import TestCase
from pynformatics.view.problem import problem_runs


class TestView__problem_runs(TestCase):
    def setUp(self):
        super(TestView__problem_runs, self).setUp()

        self.user1 = SimpleUser(ejudge_id=0)
        self.user2 = SimpleUser(ejudge_id=1)
        self.problem = EjudgeProblem(
            ejudge_prid=2,
            contest_id=3,
            ejudge_contest_id=4,
            problem_id=5,
        )
        self.session.add_all([self.user1, self.user2, self.problem])
        self.session.flush()

        self.runs = [
            [
                Run(
                    run_id=i + user.ejudge_id * 3,
                    problem=self.problem,
                    user=user
                )
                for i in range(3)
            ]
            for user in [self.user1, self.user2]
        ]
        self.session.add_all(self.runs[0])  # user1 runs
        self.session.add_all(self.runs[1])  # user2 runs

        self.request.matchdict = {'problem_id': self.problem.id}
        self.mock_context = mock.Mock()
        self.mock_context.problem = self.session.query(Problem).all()[0]
        self.mock_context.user = self.user1

    def test_filters_by_user_id(self):
        with mock.patch('pynformatics.model.run.Run.serialize', autospec=True) as serialize_mock:
            serialize_mock.side_effect = lambda self, *args: self
            response = problem_runs(self.request, self.mock_context)

        assert_that(
            response.keys(),
            contains_inanyorder(0, 1, 2)
        )

    def test_filter_by_statement_id(self):
        statements = [
            Statement()
            for i in range(2)
        ]
        self.session.add_all(statements)
        self.session.flush()

        # Для двух посылок их трех у каждого пользователя задаем statement_id
        for i in range(2):
            for (statement, run) in zip(statements, self.runs[i]):
                self.session.add(PynformaticsRun(
                    run=run,
                    statement_id=statement.id
                ))

        self.request.params = {'statement_id': statements[0].id}
        with mock.patch('pynformatics.model.run.Run.serialize', autospec=True) as serialize_mock, \
                mock.patch('pynformatics.model.run.Run.get_sources', mock.Mock(return_value='')):
            serialize_mock.side_effect = lambda self, *args: self
            response = problem_runs(self.request, self.mock_context)

        assert_that(
            response.keys(),
            contains_inanyorder(0, 3)
        )
