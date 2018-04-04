# import datetime
# from hamcrest import (
#     assert_that,
#     equal_to,
# )

# from pynformatics.model.ejudge_run import EjudgeRun
# from pynformatics.model.pynformatics_run import PynformaticsRun
# from pynformatics.testutils import TestCase


# class TestAPI__notification_update_standings(TestCase):
#     def setUp(self):
#         super(TestAPI__notification_update_standings, self).setUp()

#         self.create_problems()
#         self.create_statements()
#         self.create_users()

#     def send_request(self,
#                      run=None):
#         contest_id = 1
#         run_id = 1
#         if run:
#             contest_id = run.contest_id
#             run_id = run.run_id
#         response = self.app.get(
#             '/notification/update_standings?contest_id=%(contest_id)s&run_id=%(run_id)s&new_status=0' % {
#                 'contest_id': contest_id,
#                 'run_id': run_id,
#             }
#         )
#         return response

#     # def test_problem_standings(self):
#     #     # Создает пустую таблицу результатов, так как ее нет в базе
#     #     response = self.app.get('/problem/1/standings')
#     #     assert_that(response.json, equal_to(None))
#     #
#     #     run = Run(
#     #         run_id=1,
#     #         problem=self.problems[0],
#     #         user=self.users[0],
#     #         score=99,
#     #         status=7,
#     #     )
#     #     self.session.add(run)
#     #
#     #     self.send_request()
#     #
#     #     response = self.app.get('/problem/1/standings')
#     #     assert_that(
#     #         response.json,
#     #         equal_to({
#     #             '1': {
#     #                 'firstname': 'Maxim',
#     #                 'lastname': 'Grishkin',
#     #                 'attempts': 1,
#     #                 'score': 99,
#     #                 'status': 7,
#     #             }
#     #         })
#     #     )

#     def test_statement_standings(self):
#         response = self.app.get('/statement/1/standings')
#         assert_that(response.json, equal_to(None))

#         run = EjudgeRun(
#             run_id=1,
#             problem=self.problems[0],
#             user=self.users[0],
#             score=99,
#             status=7,
#             create_time=datetime.datetime(2018, 2, 25, 13, 57, 22)
#         )
#         pynformatics_run = PynformaticsRun(
#             run=run,
#             statement=self.statements[0],
#         )
#         self.session.add_all((run, pynformatics_run))

#         self.send_request()

#         response = self.app.get('/statement/1/standings')
#         assert_that(
#             response.json,
#             equal_to({
#                 '1': {
#                     'firstname': 'Maxim',
#                     'lastname': 'Grishkin',
#                     'runs': [
#                         {
#                             'run_id': 1,
#                             'problem_id': 1,
#                             'contest_id': 1,
#                             'score': 99,
#                             'status': 7,
#                             'create_time': '2018-02-25T13:57:22',
#                         }
#                     ]
#                 }
#             })
#         )

#     def test_required_params(self):
#         self.app.get('/notification/update_standings?run_id=1', status=400)
#         self.app.get('/notification/update_standings?contest_id=1', status=400)

#     def test_not_found(self):
#         response = self.app.get('/notification/update_standings?contest_id=1&run_id=1', status=404)
#         assert_that(
#             response.json,
#             equal_to({
#                 'code': 404,
#                 'message': 'Run not found',
#             })
#         )

