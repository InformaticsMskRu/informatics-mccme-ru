import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    has_items,
    raises,
)

from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.run import Run
from pynformatics.view.notification import notification_update_run
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import RunNotFound


class TestView__notification_update_run(TestCase):
    def setUp(self):
        super(TestView__notification_update_run, self).setUp()

        self.create_problems()
        self.create_users()

        self.ej_run = EjudgeRun(
            run_id=123,
            user=self.users[0],
            problem=self.problems[0],
        )
        self.session.add(self.ej_run)
        self.session.flush()

        self.run = Run.from_ejudge_run(self.ej_run)
        self.session.add(self.run)
        self.session.flush()
    
    def call_view(self, contest_id=None, run_id=None):
        if contest_id:
            self.request.params['contest_id'] = contest_id
        if run_id:
            self.request.params['run_id'] = run_id
        
        result = notification_update_run(self.request, mock.Mock())
        return result
    
    def test_simple(self):
        sync_mock = mock.Mock(return_value=self.run)
        notify_user_mock = mock.Mock()
        with mock.patch('pynformatics.view.notification.Run.sync', sync_mock), \
                mock.patch('pynformatics.view.notification.notify_user', notify_user_mock):
            self.call_view(contest_id=self.ej_run.contest_id, run_id=self.ej_run.run_id)
        
        sync_mock.assert_called_once_with(
            ejudge_run_id=self.ej_run.run_id,
            ejudge_contest_id=self.ej_run.contest_id,
        )
        assert_that(
            notify_user_mock.call_args[0][0], 
            equal_to(self.users[0].id)
        )
        assert_that(
            notify_user_mock.call_args[1],
            has_items('runs')
        )
    
    def test_run_not_found(self):
        assert_that(
            calling(self.call_view).with_args(contest_id=11, run_id=22),
            raises(RunNotFound),
        )
