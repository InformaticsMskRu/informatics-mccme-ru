import unittest
from types import SimpleNamespace
from unittest import mock

import requests

from pynformatics.view import contest as contest_view

RMATICS = 'http://rmatics:12346'


class FakeRequest:
    def __init__(self, **matchdict):
        self.matchdict = matchdict or {'judge_id': '2', 'contest_id': '2395', 'problem_id': '3'}
        self.registry = SimpleNamespace(settings={'rmatics.endpoint': RMATICS})


def rmatics_response(body, status_code=200, content_type='application/json'):
    resp = mock.Mock(status_code=status_code)
    resp.headers = {'Content-Type': content_type}
    resp.json.return_value = body
    return resp


class ReloadFromJudgeTests(unittest.TestCase):
    def _call(self, allowed=True, rmatics_post=None, request=None):
        with mock.patch.object(contest_view, 'RequestCheckUserCapability',
                               return_value=allowed) as caps, \
                mock.patch.object(contest_view.requests, 'post',
                                  side_effect=rmatics_post) as post:
            return contest_view.reload_from_judge(request or FakeRequest()), caps, post

    def test_forwards_to_rmatics(self):
        body = {'status': 'success', 'data': {'action': 'create'}}
        resp, caps, post = self._call(
            rmatics_post=lambda *a, **kw: rmatics_response(body))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json_body, body)
        self.assertEqual(resp.content_type, 'application/json')
        url, = post.call_args[0]
        self.assertEqual(url, '{}/contest/ejudge/2/reload/2395/3'.format(RMATICS))
        self.assertEqual(caps.call_args[0][1], 'local/pynformatics:contest_reload')

    def test_forwards_contest_reload(self):
        request = FakeRequest(judge_id='2', contest_id='2395')
        _, _, post = self._call(
            rmatics_post=lambda *a, **kw: rmatics_response({}), request=request)

        url, = post.call_args[0]
        self.assertEqual(url, '{}/contest/ejudge/2/reload/2395'.format(RMATICS))

    def test_rmatics_error_status_is_kept(self):
        body = {'status': 'error', 'code': 502, 'error': 'ejudge is down'}
        resp, _, _ = self._call(
            rmatics_post=lambda *a, **kw: rmatics_response(body, 502))

        self.assertEqual(resp.status_code, 502)
        self.assertEqual(resp.json_body, body)

    def test_non_json_reply_is_not_passed_through(self):
        html = rmatics_response(None, 500, content_type='text/html')
        html.json.side_effect = ValueError('not json')
        resp, _, _ = self._call(rmatics_post=lambda *a, **kw: html)

        self.assertEqual(resp.status_code, 502)
        self.assertEqual(resp.content_type, 'application/json')

    def test_denied_without_capability(self):
        resp, _, post = self._call(allowed=False)

        self.assertEqual(resp.status_code, 403)
        post.assert_not_called()

    def test_rmatics_unavailable(self):
        def down(*args, **kwargs):
            raise requests.ConnectionError('down')

        resp, _, _ = self._call(rmatics_post=down)

        self.assertEqual(resp.status_code, 502)
        self.assertEqual(resp.json_body['message'], 'rmatics is unavailable')


if __name__ == '__main__':
    unittest.main()
