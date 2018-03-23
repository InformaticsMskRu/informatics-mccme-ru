import datetime
import mock
import sys
from hamcrest import (
    assert_that,
    anything,
    contains_inanyorder,
    calling,
    equal_to,
    has_entries,
    is_not,
    raises,
)
from transaction.interfaces import DoomedTransaction

from pynformatics.model.run import Run
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.testutils import TestCase


if 'pynformatics.contest.ejudge.submit_queue.submit' in sys.modules:
    del sys.modules['pynformatics.contest.ejudge.submit_queue.submit']
with mock.patch('pynformatics.contest.ejudge.ejudge_proxy.submit') as ejudge_submit_mock, \
        mock.patch('pynformatics.utils.notify.notify_user') as notify_user_mock:
    from pynformatics.contest.ejudge.submit_queue.submit import Submit


class TestEjudge__submit_queue_submit_send(TestCase):
    def setUp(self):
        super(TestEjudge__submit_queue_submit_send, self).setUp()

        ejudge_submit_mock.reset_mock()
        notify_user_mock.reset_mock()

        self.create_users()
        self.create_problems()
        self.create_statements()

        self.run = EjudgeRun(
            run_id=12,
            user=self.users[0],
            problem=self.problems[0],
        )
        self.session.add(self.run)
        self.session.flush([self.run])

        self.file_mock = mock.Mock()
        self.file_mock.value.decode.return_value = 'source'
        self.file_mock.filename = 'filename'

        self.context_mock = mock.Mock()
        self.context_mock.user = self.users[0]
        self.context_mock.problem = self.problems[0]
        self.context_mock.statement_id = self.statements[0].id

    def test_simple(self):
        submit = Submit(
            id=1,
            context=self.context_mock,
            create_time=datetime.datetime(2018, 3, 30, 16, 59, 0),
            file=self.file_mock,
            language_id=27,
            ejudge_url='ejudge_url',
        )

        ejudge_submit_mock.return_value = {
            'code': 0,
            'run_id': self.run.run_id,
        }

        # Отправка задачи должна закоммитить созданную посылку, в тестах это вызывает ошибку
        assert_that(
            calling(submit.send).with_args(),
            raises(DoomedTransaction)
        )

        ejudge_submit_mock.assert_called_once_with(
            run_file=self.file_mock.file,
            contest_id=1,
            prob_id=1,
            lang_id=27,
            login=None,
            password=None,
            filename='filename',
            url='ejudge_url',
            user_id=1,
        )

        run = self.session.query(Run).one()
        assert_that(run.user.id, equal_to(self.users[0].id))
        assert_that(run.problem.id, equal_to(self.problems[0].id))
        assert_that(run.create_time, equal_to(submit.create_time))

        assert_that(
            notify_user_mock.call_args_list[0][1],
            has_entries({
                'user_id': 1,
                'runs': [
                    {
                        'id': 1,
                        'problem_id': 1,
                        'statement_id': 1,
                        'score': None,
                        'status': None,
                        'language_id': 27,
                        'create_time': '2018-03-30 16:59:00',
                    }
                ],
                'event': {
                    'type': 'RUN_CREATED_FROM_SUBMIT',
                    'submit_id': submit.id,
                }
            })
        )

    def test_handles_submit_exception(self):
        # В случае, если функция submit бросила исключение
        submit = Submit(
            id=1,
            context=self.context_mock,
            create_time=datetime.datetime(2018, 3, 30, 17, 10, 11),
            file=self.file_mock,
            language_id=27,
            ejudge_url='ejudge_url',
        )

        ejudge_submit_mock.side_effect = lambda *args, **kwargs: 1 / 0
        assert_that(
            calling(submit.send),
            is_not(raises(anything())),
        )

        notify_user_mock.assert_called_once_with(
            user_id=self.users[0].id,
            message={
                'ejudge_error': {
                    'code': None,
                    'message': 'Ошибка отправки задачи'
                }
            }
        )

        ejudge_submit_mock.side_effect = None

    def test_handles_submit_error(self):
        # В случае, если ejudge вернул не 0 код

        submit = Submit(
            id=1,
            context=self.context_mock,
            create_time=datetime.datetime(2018, 3, 30, 17, 10, 11),
            file=self.file_mock,
            language_id=27,
            ejudge_url='ejudge_url',
        )

        ejudge_submit_mock.return_value = {
            'code': 123,
            'message': 'some message',
            'other': 'secrets'
        }
        assert_that(
            calling(submit.send),
            is_not(raises(anything())),
        )

        notify_user_mock.assert_called_once_with(
            user_id=self.users[0].id,
            message={
                'ejudge_error': {
                    'code': 123,
                    'message': 'some message'
                }
            }
        )

        ejudge_submit_mock.side_effect = None
