import mock
from hamcrest import (
    assert_that,
    has_entries,
)

from pynformatics.testutils import (
    TestCase,
    dummy_decorator,
)
mock.patch('pynformatics.utils.check_role.check_global_role', dummy_decorator).start()

from pynformatics.view.protocol import protocol_get_full
from pynformatics.model import EjudgeRun


class TestView__protocol_get_full(TestCase):
    def setUp(self):
        super(TestView__protocol_get_full, self).setUp()

        self.contest_id = 1234
        self.run_id = 5678
        self.request.matchdict = {
            'contest_id': self.contest_id,
            'run_id': self.run_id
        }

    def _get_mocked_run(self,
                        count,
                        status_string,
                        ):
        """
        Создает замоканый run
        """
        run = mock.Mock()
        run.user.statement.filter = lambda *args: run.user.statement
        run.user.statement.count = lambda *args: count
        run.status_string = status_string
        run.tests = {}
        return run

    def test_compilation_error(self):
        run = self._get_mocked_run(count=0, status_string='CE')
        compiler_output = 'mocked compiler output'
        run.compiler_output = compiler_output

        with mock.patch.object(EjudgeRun, 'get_by', mock.Mock(return_value=run)):
            result = protocol_get_full(self.request)

        assert_that(
            result,
            has_entries({
                'compiler_output': compiler_output,
            })
        )
