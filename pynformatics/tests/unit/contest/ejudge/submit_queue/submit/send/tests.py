import mock
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

from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.model.run import Run
from pynformatics.testutils import TestCase

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

        self.run = Run(
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
            context=self.context_mock,
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

        run = self.session.query(PynformaticsRun).one()
        assert_that(run.run_id, equal_to(self.run.run_id))
        assert_that(run.contest_id, equal_to(1))
        assert_that(run.statement, equal_to(self.statements[0]))
        assert_that(run.source, equal_to('source'))

        assert_that(
            notify_user_mock.call_args_list[0][1],
            has_entries({
                'user_id': 1,
                'runs': contains_inanyorder(
                    has_entries({'run_id': self.run.run_id})
                )
            })
        )

    def test_handles_submit_exception(self):
        # В случае, если функция submit бросила исключение
        submit = Submit(
            context=self.context_mock,
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
            data={
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
            context=self.context_mock,
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
            data={
                'ejudge_error': {
                    'code': 123,
                    'message': 'some message'
                }
            }
        )

        ejudge_submit_mock.side_effect = None
