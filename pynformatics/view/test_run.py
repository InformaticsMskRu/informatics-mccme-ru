import unittest
from types import SimpleNamespace
from unittest import mock

from pynformatics.view import run as run_view

RMATICS = 'http://rmatics:12346'


class FakeResponse:
    def __init__(self):
        self.status = 200


class FakeRequest:
    def __init__(self, run_id=7):
        self.matchdict = {'run_id': str(run_id)}
        self.response = FakeResponse()
        self.registry = SimpleNamespace(settings={'rmatics.endpoint': RMATICS})


def rmatics_response(payload, status='success'):
    resp = mock.Mock()
    resp.json.return_value = {'status': status, 'status_code': 200, 'data': payload}
    return resp


class GetRunStatusTests(unittest.TestCase):
    def _call(self, request, params, rmatics_get):
        """Вызвать вьюху с замоканными проверкой прав и походом в rmatics."""
        with mock.patch.object(run_view, 'GetUserCourseContextParams',
                               return_value=params) as caps, \
                mock.patch.object(run_view.requests, 'get',
                                  side_effect=rmatics_get) as get:
            return run_view.get_run_status(request), caps, get

    def test_returns_two_numbers(self):
        request = FakeRequest()
        result, _, get = self._call(
            request, {'user_id': 1, 'is_admin': False},
            lambda *a, **kw: rmatics_response({'ejudge_status': 7, 'ejudge_score': 40}))

        self.assertEqual(result, {'ejudge_status': 7, 'ejudge_score': 40})
        url, = get.call_args[0]
        self.assertEqual(url, '{}/problem/run/7/status'.format(RMATICS))
        # права, посчитанные moodle-стороной, уезжают в rmatics
        self.assertEqual(get.call_args[1]['params'], {'user_id': 1, 'is_admin': False})

    def test_null_score_is_preserved(self):
        result, _, _ = self._call(
            FakeRequest(), {'user_id': 1},
            lambda *a, **kw: rmatics_response({'ejudge_status': 377, 'ejudge_score': None}))

        self.assertIsNone(result['ejudge_score'])

    def test_not_authorized(self):
        result, _, get = self._call(FakeRequest(), None, lambda *a, **kw: None)

        self.assertEqual(result['result'], 'error')
        get.assert_not_called()

    def test_rmatics_error_is_passed_through(self):
        def not_found(*a, **kw):
            resp = mock.Mock()
            resp.json.return_value = {'status': 'error', 'code': 404,
                                      'error': 'Run with id #7 is not found'}
            return resp

        result, _, _ = self._call(FakeRequest(), {'user_id': 1}, not_found)

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['code'], 404)

    def test_rmatics_unavailable(self):
        request = FakeRequest()

        def boom(*a, **kw):
            raise Exception('connection refused')

        result, _, _ = self._call(request, {'user_id': 1}, boom)

        self.assertEqual(result['result'], 'error')
        self.assertEqual(request.response.status, 500)


if __name__ == '__main__':
    unittest.main()
