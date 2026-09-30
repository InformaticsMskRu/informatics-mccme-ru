import base64
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

import requests

from pynformatics.view import contest as contest_view

RMATICS = 'http://rmatics:12346'


class FakeRequest:
    def __init__(self, probpics_dir=None, **matchdict):
        self.matchdict = matchdict or {'judge_id': '2', 'contest_id': '2395', 'problem_id': '3'}
        settings = {'rmatics.endpoint': RMATICS}
        if probpics_dir:
            settings['moodle.probpics_dir'] = probpics_dir
        self.registry = SimpleNamespace(settings=settings)


def b64(data):
    return base64.b64encode(data).decode()


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


class StoreStatementImagesTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = tmp.name

    def _call(self, data, status_code=200, request=None):
        body = {'status': 'success' if status_code == 200 else 'error', 'data': data}
        with mock.patch.object(contest_view, 'RequestCheckUserCapability', return_value=True), \
                mock.patch.object(contest_view.requests, 'post',
                                  return_value=rmatics_response(body, status_code)):
            return contest_view.reload_from_judge(request or FakeRequest(probpics_dir=self.dir))

    def read(self, *path):
        with open(os.path.join(self.dir, *path), 'rb') as f:
            return f.read()

    def test_rmatics_log_is_extended(self):
        resp = self._call({'action': 'create', 'log': ['0.01s info: done'], 'problems': [
            {'id': 42, 'name': 'Sum', 'images': {'a.png': b64(b'A')}}]})

        log_lines = resp.json_body['data']['log']
        self.assertEqual(log_lines[0], '0.01s info: done')
        self.assertTrue(log_lines[1].startswith('pynformatics info: stored 1 statement image(s)'))

    def test_problem_reload_images(self):
        resp = self._call({'action': 'create', 'statement': 'imported', 'problems': [
            {'id': 42, 'name': 'Sum', 'images': {'a.png': b64(b'A'), 'b.png': b64(b'B')}}]})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.read('42', 'a.png'), b'A')
        self.assertEqual(self.read('42', 'b.png'), b'B')
        # the reply lists the stored files instead of their content
        self.assertEqual(resp.json_body['data']['problems'][0]['images'], ['a.png', 'b.png'])
        self.assertEqual(resp.json_body['data']['log'][-1],
                         'pynformatics info: stored 2 statement image(s) of problem 42 in '
                         '{}: a.png, b.png'.format(os.path.join(self.dir, '42')))

    def test_contest_reload_images(self):
        resp = self._call({'problems': [
            {'action': 'create', 'problems': [{'id': 1, 'name': 'A', 'images': {'p.png': b64(b'1')}}]},
            {'action': 'update', 'problems': [{'id': 2, 'name': 'B'}]},
        ]}, request=FakeRequest(probpics_dir=self.dir, judge_id='2', contest_id='2395'))

        self.assertEqual(self.read('1', 'p.png'), b'1')
        self.assertFalse(os.path.exists(os.path.join(self.dir, '2')))
        results = resp.json_body['data']['problems']
        self.assertEqual(results[0]['problems'][0]['images'], ['p.png'])
        self.assertNotIn('images', results[1]['problems'][0])

    def test_names_stay_in_the_problem_dir(self):
        resp = self._call({'action': 'create', 'problems': [
            {'id': 42, 'name': 'Sum', 'images': {'../../x.png': b64(b'X'), '.htaccess': b64(b'H')}}]})

        self.assertEqual(os.listdir(self.dir), ['42'])
        self.assertEqual(os.listdir(os.path.join(self.dir, '42')), ['x.png'])
        self.assertEqual(resp.json_body['data']['problems'][0]['images'], ['x.png'])
        self.assertIn("pynformatics warning: skipped statement image '.htaccess' of problem 42",
                      resp.json_body['data']['log'])

    def test_error_reply_is_not_processed(self):
        resp = self._call({'action': 'create', 'problems': [
            {'id': 42, 'name': 'Sum', 'images': {'a.png': b64(b'A')}}]}, status_code=409)

        self.assertEqual(resp.status_code, 409)
        self.assertEqual(os.listdir(self.dir), [])

    def test_write_failure(self):
        blocker = os.path.join(self.dir, 'file')
        open(blocker, 'w').close()

        resp = self._call({'action': 'create', 'problems': [
            {'id': 42, 'name': 'Sum', 'images': {'a.png': b64(b'A')}}]},
            request=FakeRequest(probpics_dir=blocker))

        self.assertEqual(resp.status_code, 500)
        self.assertEqual(resp.json_body['message'], 'Failed to store statement images')


if __name__ == '__main__':
    unittest.main()
