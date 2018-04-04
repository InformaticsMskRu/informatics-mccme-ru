# import datetime
# import mock
# from hamcrest import (
#     assert_that,
#     calling,
#     equal_to,
#     raises,
# )

# from pynformatics.model.pynformatics_run import PynformaticsRun
# from pynformatics.model.ejudge_run import EjudgeRun
# from pynformatics.model.standings import (
#     ProblemStandings,
#     StatementStandings,
# )
# from pynformatics.testutils import TestCase
# from pynformatics.utils.exceptions import RunNotFound
# from pynformatics.view.notification import notification_update_standings


# class TestView__notification_update_standings(TestCase):
#     def setUp(self):
#         super(TestView__notification_update_standings, self).setUp()

#         self.create_problems()
#         self.create_statements()
#         self.create_users()

#     def call_view(self, run_id, contest_id):
#         self.request.params = {
#             'run_id': run_id,
#             'contest_id': contest_id,
#         }

#         problem_update_mock = mock.Mock()
#         statement_update_mock = mock.Mock()
#         with mock.patch.object(ProblemStandings, 'update', problem_update_mock), \
#                 mock.patch.object(StatementStandings, 'update', statement_update_mock):
#             result = notification_update_standings(self.request)
#         assert_that(
#             result,
#             equal_to({})
#         )
#         return problem_update_mock, statement_update_mock

#     def test_nothing_to_update(self):
#         # Таблиц результатов нет, обновлять ничего не нужно
#         run = EjudgeRun(
#             run_id=1,
#             problem=self.problems[0],
#             user=self.users[0],
#             score=100,
#             status=0,
#             create_time=datetime.datetime(2018, 2, 25, 14, 10, 11),
#         )
#         self.session.add(run)
#         self.session.flush()

#         problem_update_mock, statement_update_mock = self.call_view(
#             run_id=run.run_id,
#             contest_id=run.contest_id
#         )
#         problem_update_mock.assert_not_called()
#         statement_update_mock.assert_not_called()

#     # def test_problem_standings(self):
#     #     # Есть таблица результатов для задачи, обновляется только она
#     #     ProblemStandings.create(problem=self.problems[0])

#     #     run = EjudgeRun(
#     #         run_id=1,
#     #         problem=self.problems[0],
#     #         user=self.users[0],
#     #         score=100,
#     #         status=0,
#     #         create_time=datetime.datetime(2018, 2, 25, 14, 10, 11),
#     #     )
#     #     pynformatics_run = PynformaticsRun(run=run, statement=self.statements[0])
#     #     self.session.add_all((run, pynformatics_run))
#     #     self.session.flush()

#     #     problem_update_mock, statement_update_mock = self.call_view(
#     #         run_id=run.run_id,
#     #         contest_id=run.contest_id
#     #     )
#     #     problem_update_mock.assert_called_once_with(self.users[0])
#     #     statement_update_mock.assert_not_called()

#     def test_statement_standings(self):
#         # Есть таблица результатов для контеста, обновляется только она
#         StatementStandings.create(statement=self.statements[0])

#         run = EjudgeRun(
#             run_id=1,
#             problem=self.problems[0],
#             user=self.users[0],
#             score=100,
#             status=0,
#             create_time=datetime.datetime(2018, 2, 25, 14, 10, 11),
#         )
#         pynformatics_run = PynformaticsRun(run=run, statement=self.statements[0])
#         self.session.add_all((run, pynformatics_run))
#         self.session.flush()

#         problem_update_mock, statement_update_mock = self.call_view(
#             run_id=run.run_id,
#             contest_id=run.contest_id
#         )
#         problem_update_mock.assert_not_called()
#         statement_update_mock.assert_called_once_with(run)

#     # def test_both_standings(self):
#     #     ProblemStandings.create(problem=self.problems[0])
#     #     StatementStandings.create(statement=self.statements[0])

#     #     run = EjudgeRun(
#     #         run_id=1,
#     #         problem=self.problems[0],
#     #         user=self.users[0],
#     #         score=100,
#     #         status=0,
#     #         create_time=datetime.datetime(2018, 2, 25, 14, 10, 11),
#     #     )
#     #     pynformatics_run = PynformaticsRun(run=run, statement=self.statements[0])
#     #     self.session.add_all((run, pynformatics_run))
#     #     self.session.flush()

#     #     problem_update_mock, statement_update_mock = self.call_view(
#     #         run_id=run.run_id,
#     #         contest_id=run.contest_id
#     #     )
#     #     problem_update_mock.assert_called_once_with(self.users[0])
#     #     statement_update_mock.assert_called_once_with(run)

#     # def test_standings_matching(self):
#     #     # Таблицы результатов есть, но для других задач и контестов
#     #     ProblemStandings.create(problem=self.problems[1])
#     #     StatementStandings.create(statement=self.statements[1])

#     #     run = EjudgeRun(
#     #         run_id=1,
#     #         problem=self.problems[0],
#     #         user=self.users[0],
#     #         score=100,
#     #         status=0,
#     #         create_time=datetime.datetime(2018, 2, 25, 14, 10, 11),
#     #     )
#     #     self.session.add(run)
#     #     self.session.flush()

#     #     problem_update_mock, statement_update_mock = self.call_view(
#     #         run_id=run.run_id,
#     #         contest_id=run.contest_id
#     #     )
#     #     problem_update_mock.assert_not_called()
#     #     statement_update_mock.assert_not_called()

#     def test_not_found(self):
#         assert_that(
#             calling(self.call_view).with_args(run_id=1, contest_id=1),
#             raises(RunNotFound)
#         )

