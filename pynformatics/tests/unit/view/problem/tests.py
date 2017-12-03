import mock
from hamcrest import (
    assert_that,
    calling,
    raises,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import Forbidden
from pynformatics.view.problem import problem_submits_v2


class TestView__problem_submits_v2(TestCase):
    def setUp(self):
        super(TestView__problem_submits_v2, self).setUp()

        self.ejudge_submit_patcher = mock.patch('pynformatics.view.problem.submit', mock.Mock())
        self.ejudge_submit_patcher.start()

        self.check_auth_patcher = mock.patch.object(Context, 'check_auth', mock.Mock())
        self.check_auth_patcher.start()

        self.request.registry.settings['ejudge.new_client_url'] = ''
        self.request.POST = {'file': mock.Mock()}

        self.get_languages_patcher = mock.patch.object(Context, 'get_allowed_languages')
        self.get_languages_mock = self.get_languages_patcher.start()

    def tearDown(self):
        super(TestView__problem_submits_v2, self).tearDown()
        self.ejudge_submit_patcher.stop()
        self.check_auth_patcher.stop()
        self.get_languages_patcher.stop()

    def test_not_allowed_language(self):
        """
        Tries to submit problem with not allowed language id. Must raise 401 Forbidden
        """
        allowed_languages = ['1', '2']
        lang_id = '3'
        self.get_languages_mock.return_value = allowed_languages
        self.request.params = {'lang_id': lang_id}
        assert_that(
            calling(problem_submits_v2).with_args(self.request),
            raises(Forbidden),
        )
