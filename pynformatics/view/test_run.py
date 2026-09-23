import unittest
from types import SimpleNamespace
from unittest import mock

from pyramid import testing

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

    def test_returns_verdict_score_and_test_num(self):
        request = FakeRequest()
        result, _, get = self._call(
            request, {'user_id': 1, 'is_admin': False},
            lambda *a, **kw: rmatics_response({'ejudge_status': 7, 'ejudge_score': 40,
                                              'ejudge_test_num': 3}))

        self.assertEqual(result, {'ejudge_status': 7, 'ejudge_score': 40,
                                  'ejudge_test_num': 3})
        url, = get.call_args[0]
        self.assertEqual(url, '{}/problem/run/7/status'.format(RMATICS))
        # права, посчитанные moodle-стороной, уезжают в rmatics
        self.assertEqual(get.call_args[1]['params'], {'user_id': 1, 'is_admin': False})

    def test_null_score_is_preserved(self):
        result, _, _ = self._call(
            FakeRequest(), {'user_id': 1},
            lambda *a, **kw: rmatics_response({'ejudge_status': 377, 'ejudge_score': None,
                                              'ejudge_test_num': None}))

        self.assertIsNone(result['ejudge_score'])
        self.assertIsNone(result['ejudge_test_num'])

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


class UpdateRunFromEjudgeV2Tests(unittest.TestCase):
    BODY = b'{"run_id": 7, "run_uuid": "u", "contest_id": 3, "status": 0, "judge_id": 1}'

    def _request(self, content_type='application/json', **headers):
        request = testing.DummyRequest(method='POST', headers=headers)
        request.body = self.BODY
        request.content_type = content_type
        request.registry.settings = {'rmatics.endpoint': RMATICS}
        return request

    def _call(self, request, rmatics_post):
        with mock.patch.object(run_view.requests, 'post',
                               side_effect=rmatics_post) as post:
            return run_view.update_run_from_ejudge_v2(request), post

    @staticmethod
    def _rmatics(status_code, body=b'{}', content_type='application/json'):
        resp = mock.Mock()
        resp.status_code = status_code
        resp.content = body
        resp.headers = {'Content-Type': content_type}
        return lambda *a, **kw: resp

    def test_forwards_body_and_token(self):
        request = self._request(Authorization='Bearer judge-1-token')
        response, post = self._call(request, self._rmatics(200, b'[{}, 200]'))

        url, = post.call_args[0]
        self.assertEqual(url, '{}/problem/run/action/update_from_ejudge_v2'.format(RMATICS))
        self.assertEqual(post.call_args[1]['data'], self.BODY)
        self.assertEqual(post.call_args[1]['headers']['Authorization'], 'Bearer judge-1-token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'[{}, 200]')

    def test_rmatics_rejection_keeps_status_code(self):
        # notify-worker treats non-2xx as a failed notification
        response, _ = self._call(
            self._request(Authorization='Bearer wrong-token'),
            self._rmatics(401, b'{"message": "Bearer token is required"}',
                          'application/json; charset=utf-8'))

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.headers['Content-Type'], 'application/json; charset=utf-8')

    def test_no_authorization_header(self):
        response, post = self._call(self._request(), self._rmatics(200))

        self.assertEqual(response.status_code, 403)
        post.assert_not_called()

    def test_no_content_type(self):
        response, post = self._call(
            self._request(content_type='', Authorization='Bearer t'), self._rmatics(200))

        self.assertEqual(response.status_code, 400)
        post.assert_not_called()

    def test_non_json_content_type(self):
        response, post = self._call(
            self._request(content_type='text/plain', Authorization='Bearer t'), self._rmatics(200))

        self.assertEqual(response.status_code, 400)
        post.assert_not_called()

    def test_rmatics_unavailable(self):
        def boom(*a, **kw):
            raise Exception('connection refused')

        response, _ = self._call(self._request(Authorization='Bearer t'), boom)

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json_body['result'], 'error')


if __name__ == '__main__':
    unittest.main()
