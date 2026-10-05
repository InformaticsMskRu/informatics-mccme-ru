import hashlib
import json
import unittest
from types import SimpleNamespace
from unittest import mock

from pynformatics.utils.api_token import API_CONTEXT_BASE, parse_api_tokens
from pynformatics.view import api as api_view

SECRET = 'good-secret'


def token_entry(**overrides):
    entry = {
        'id': 7,
        'name': 'bot',
        'sha256': hashlib.sha256(SECRET.encode()).hexdigest(),
        'user_ids': None,
        'problems': None,
    }
    entry.update(overrides)
    return entry


class FakeRequest:
    def __init__(self, tokens, headers=None, params=None, post=None, matchdict=None):
        self.headers = headers if headers is not None else {'Authorization': 'Bearer ' + SECRET}
        self.params = params or {}
        self.POST = post or {}
        self.matchdict = matchdict or {}
        self.registry = SimpleNamespace(settings={
            'rmatics.endpoint': 'http://rmatics.test',
            'api.tokens': tokens,
        })


def rmatics_reply(payload, status=200):
    resp = mock.Mock()
    resp.status_code = status
    resp.json.return_value = payload
    resp.content = json.dumps(payload).encode()
    return resp


class ParseTokensTests(unittest.TestCase):
    def _parse(self, **overrides):
        return parse_api_tokens({'api.tokens': [token_entry(**overrides)]})

    def test_valid_token(self):
        token = self._parse(user_ids=[10, 11], problems=[1])[0]
        self.assertEqual(token.context_source, API_CONTEXT_BASE + 7)
        self.assertTrue(token.allows_user(10))
        self.assertFalse(token.allows_user(12))

    def test_null_allows_any_user_but_not_system_ones(self):
        token = self._parse()[0]
        self.assertTrue(token.allows_user(12345))
        self.assertFalse(token.allows_user(2))

    def test_missing_user_ids_or_problems_is_rejected(self):
        for key in ('user_ids', 'problems'):
            entry = token_entry()
            del entry[key]
            with self.assertRaises(ValueError):
                parse_api_tokens({'api.tokens': [entry]})

    def test_bad_entries_are_rejected(self):
        for overrides in ({'id': 0}, {'sha256': 'abc'}, {'user_ids': [2]}, {'problems': 'x'}):
            with self.assertRaises(ValueError):
                self._parse(**overrides)
        with self.assertRaises(ValueError):
            parse_api_tokens({'api.tokens': [token_entry(), token_entry()]})

    def test_no_setting_means_no_tokens(self):
        self.assertEqual(parse_api_tokens({}), [])


class SubmitTests(unittest.TestCase):
    def _submit(self, tokens=None, headers=None, params=None, file=True, reply=None, raises=None):
        tokens = [token_entry()] if tokens is None else tokens
        params = {'user_id': '101', 'lang_id': '27', **(params or {})}
        post = {'file': SimpleNamespace(file=mock.Mock())} if file else {}
        request = FakeRequest(tokens, headers=headers, params=params, post=post,
                              matchdict={'problem_id': '42'})
        reply = reply or rmatics_reply({'status': 'success', 'data': {'run_id': 9}})
        with mock.patch.object(api_view.requests, 'post', return_value=reply,
                               side_effect=raises) as post_mock:
            response = api_view.api_problem_submit(request)
        return response, post_mock

    def test_submit_forwards_user_and_token_context(self):
        response, post = self._submit()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body, {'run_id': 9})
        self.assertEqual(post.call_args[0][0], 'http://rmatics.test/problem/trusted/42/submit_v2')
        self.assertEqual(post.call_args[1]['data'], {
            'lang_id': 27, 'user_id': 101, 'context_source': API_CONTEXT_BASE + 7})

    def test_client_context_and_statement_are_ignored(self):
        _, post = self._submit(params={'context_source': '5', 'statement_id': '3', 'is_visible': '0'})
        data = post.call_args[1]['data']
        self.assertEqual(data['context_source'], API_CONTEXT_BASE + 7)
        self.assertNotIn('statement_id', data)
        self.assertNotIn('is_visible', data)

    def test_missing_or_malformed_authorization_is_401(self):
        for headers in ({}, {'Authorization': 'Basic abc'}, {'Authorization': 'Bearer '}):
            response, post = self._submit(headers=headers)
            self.assertEqual(response.status_code, 401)
            post.assert_not_called()

    def test_wrong_token_is_401(self):
        response, post = self._submit(headers={'Authorization': 'Bearer nope'})
        self.assertEqual(response.status_code, 401)
        post.assert_not_called()

    def test_user_outside_allowlist_is_403(self):
        response, post = self._submit(tokens=[token_entry(user_ids=[1000])])
        self.assertEqual(response.status_code, 403)
        post.assert_not_called()

    def test_system_user_is_403_even_for_any_user_token(self):
        response, _ = self._submit(params={'user_id': '2'})
        self.assertEqual(response.status_code, 403)

    def test_problem_outside_allowlist_is_403(self):
        response, post = self._submit(tokens=[token_entry(problems=[1])])
        self.assertEqual(response.status_code, 403)
        post.assert_not_called()

    def test_missing_fields_are_400(self):
        for params in ({'user_id': 'x'}, {'lang_id': 'x'}):
            response, _ = self._submit(params=params)
            self.assertEqual(response.status_code, 400)
        response, _ = self._submit(file=False)
        self.assertEqual(response.status_code, 400)

    def test_rmatics_error_is_passed_through(self):
        payload = {'status': 'error', 'code': 400, 'error': 'Source file is duplicate'}
        response, _ = self._submit(reply=rmatics_reply(payload, status=400))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.body), payload)

    def test_rmatics_down_is_502(self):
        response, _ = self._submit(raises=OSError('down'))
        self.assertEqual(response.status_code, 502)


class StatusTests(unittest.TestCase):
    def _status(self, reply=None, headers=None, raises=None):
        request = FakeRequest([token_entry()], headers=headers, matchdict={'run_id': '9'})
        reply = reply or rmatics_reply({'status': 'success', 'data': {
            'ejudge_status': 0, 'ejudge_score': 100, 'ejudge_test_num': None}})
        with mock.patch.object(api_view.requests, 'get', return_value=reply,
                               side_effect=raises) as get:
            response = api_view.api_run_status(request)
        return response, get

    def test_status_is_scoped_to_token_context_without_user(self):
        response, get = self._status()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body['ejudge_score'], 100)
        self.assertEqual(get.call_args[0][0], 'http://rmatics.test/problem/run/9/status')
        self.assertEqual(get.call_args[1]['params'], {
            'is_admin': 'false', 'context_source': API_CONTEXT_BASE + 7})

    def test_unauthorized_is_401(self):
        response, get = self._status(headers={})
        self.assertEqual(response.status_code, 401)
        get.assert_not_called()

    def test_foreign_run_is_404(self):
        payload = {'status': 'error', 'code': 404, 'error': 'Run with id #9 is not found'}
        response, _ = self._status(reply=rmatics_reply(payload, status=404))
        self.assertEqual(response.status_code, 404)

    def test_rmatics_down_is_502(self):
        response, _ = self._status(raises=OSError('down'))
        self.assertEqual(response.status_code, 502)


if __name__ == '__main__':
    unittest.main()
