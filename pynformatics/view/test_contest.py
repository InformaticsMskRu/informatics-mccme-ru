import unittest
from types import SimpleNamespace
from unittest import mock

import requests

from pynformatics.view import contest as contest_view

RMATICS = 'http://rmatics:12346'


class FakeRequest:
    def __init__(self):
        self.matchdict = {'judge_id': '2', 'contest_id': '2395', 'problem_id': '3'}
        self.registry = SimpleNamespace(settings={'rmatics.endpoint': RMATICS})


def rmatics_response(body, status_code=200):
    resp = mock.Mock(content=body, status_code=status_code)
    resp.headers = {'Content-Type': 'application/json'}
    return resp


class ReloadProblemFromJudgeTests(unittest.TestCase):
    def _call(self, allowed=True, rmatics_post=None):
        with mock.patch.object(contest_view, 'RequestCheckUserCapability',
                               return_value=allowed) as caps, \
                mock.patch.object(contest_view.requests, 'post',
                                  side_effect=rmatics_post) as post:
            return contest_view.reload_problem_from_judge(FakeRequest()), caps, post

    def test_forwards_to_rmatics(self):
        body = b'{"status": "success", "data": {"action": "create"}}'
        resp, caps, post = self._call(
            rmatics_post=lambda *a, **kw: rmatics_response(body))

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.body, body)
        self.assertEqual(resp.content_type, 'application/json')
        url, = post.call_args[0]
        self.assertEqual(url, '{}/contest/ejudge/2/reload/2395/3'.format(RMATICS))
        self.assertEqual(caps.call_args[0][1], 'local/pynformatics:contest_reload')

    def test_rmatics_error_status_is_kept(self):
        body = b'{"status": "error", "code": 502, "error": "ejudge is down"}'
        resp, _, _ = self._call(
            rmatics_post=lambda *a, **kw: rmatics_response(body, 502))

        self.assertEqual(resp.status_code, 502)
        self.assertEqual(resp.body, body)

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
