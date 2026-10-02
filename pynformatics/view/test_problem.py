import unittest
from types import SimpleNamespace
from unittest import mock

from pynformatics.view import problem as problem_view


class FakeResponse:
    def __init__(self):
        self.status = 200


class FakeRequest:
    def __init__(self, problem_id, settings=None, params=None):
        self.matchdict = {'problem_id': problem_id}
        self.response = FakeResponse()
        self.registry = SimpleNamespace(settings=settings or {})
        self.params = params or {}
        self.cookies = {}


def make_problem(**overrides):
    # A plain Problem row: it deliberately does NOT carry the ejudge columns —
    # those live on mdl_ejudge_problem (EjudgeProblemDummy), fetched separately.
    attrs = dict(
        id=42,
        name='A+B',
        content='<p>statement</p>',
        sample_tests_html='<pre>1 2</pre>',
        output_only=False,
        show_limits=True,
        timelimit=1.0,
        memorylimit=268435456,
        sample_tests='1,2',
        description='problem description',
        analysis='problem analysis',
        pr_id=555,
    )
    attrs.update(overrides)
    # SimpleNamespace rather than Mock: Mock reserves the name kwarg for the
    # mock's own label, so problem.name would return a child mock, not the value.
    return SimpleNamespace(**attrs)


def make_ejudge(**overrides):
    # The mdl_ejudge_problem row (EjudgeProblemDummy) with the ejudge columns.
    attrs = dict(
        ejudge_prid=555,
        ejudge_contest_id=100,
        short_id='A',
        judges_settings=None,
    )
    attrs.update(overrides)
    return SimpleNamespace(**attrs)


class ProblemGetTests(unittest.TestCase):
    def _call(self, request, problem=None, ejudge=None, caps=None, query_raises=None,
              statement=None):
        """Invoke problem_get with DBSession and capability checks mocked.

        The base Problem query returns `problem`; the EjudgeProblemDummy query
        returns `ejudge` and the Statement query `statement`. caps maps a capability string -> bool; anything not
        listed is denied.
        """
        caps = caps or {}

        def query_for(model):
            query = mock.Mock()
            if model is problem_view.EjudgeProblemDummy:
                query.filter.return_value.first.return_value = ejudge
            elif model is problem_view.Statement:
                query.filter.return_value.first.return_value = statement
            else:
                query.filter.return_value.first.return_value = problem
            return query

        def cap_check(_request, capability, *args, **kwargs):
            return caps.get(capability, False)

        with mock.patch.object(problem_view, 'DBSession') as db, \
                mock.patch.object(problem_view, 'RequestCheckUserCapability',
                                  side_effect=cap_check):
            if query_raises is not None:
                db.query.side_effect = query_raises
            else:
                db.query.side_effect = query_for
            result = problem_view.problem_get(request)
        return result

    def test_public_fields_only(self):
        request = FakeRequest('42')
        result = self._call(request, problem=make_problem())

        self.assertEqual(request.response.status, 200)
        self.assertEqual(result['id'], 42)
        self.assertEqual(result['name'], 'A+B')
        self.assertEqual(result['content'], '<p>statement</p>')
        self.assertEqual(result['sample_tests_html'], '<pre>1 2</pre>')
        self.assertEqual(result['output_only'], False)
        # limits are public when show_limits is set
        self.assertEqual(result['timelimit'], 1.0)
        self.assertEqual(result['memorylimit'], 268435456)
        # permission-gated fields must be absent
        for hidden in ('show_limits', 'sample_tests', 'description', 'analysis'):
            self.assertNotIn(hidden, result)

    def test_limits_hidden_when_show_limits_false(self):
        request = FakeRequest('42')
        result = self._call(request, problem=make_problem(show_limits=False))

        self.assertNotIn('timelimit', result)
        self.assertNotIn('memorylimit', result)

    def test_admin_fields_with_problem_admin_capability(self):
        request = FakeRequest('42')
        result = self._call(
            request,
            problem=make_problem(),
            ejudge=make_ejudge(),
            caps={'local/pynformatics:problem_admin': True},
        )

        self.assertEqual(result['show_limits'], True)
        self.assertEqual(result['sample_tests'], '1,2')
        # ejudge service fields come from the EjudgeProblemDummy row
        self.assertEqual(result['ejudge_contest_id'], 100)
        self.assertEqual(result['short_id'], 'A')
        self.assertEqual(result['judges_settings'], [])
        # analysis capability was not granted
        self.assertNotIn('description', result)
        self.assertNotIn('analysis', result)

    def test_ejudge_service_fields_hidden_without_admin(self):
        request = FakeRequest('42')
        result = self._call(request, problem=make_problem(), ejudge=make_ejudge())

        for hidden in ('ejudge_contest_id', 'short_id', 'judges_settings'):
            self.assertNotIn(hidden, result)

    def test_ejudge_fields_absent_for_non_ejudge_problem(self):
        # A problem with no linked ejudge row (pr_id is None): no ejudge lookup,
        # no error, ejudge fields simply omitted.
        request = FakeRequest('42')
        result = self._call(
            request,
            problem=make_problem(pr_id=None),
            ejudge=None,
            caps={'local/pynformatics:problem_admin': True},
        )

        self.assertEqual(result['show_limits'], True)
        for hidden in ('ejudge_contest_id', 'short_id', 'judges_settings'):
            self.assertNotIn(hidden, result)

    def test_ejudge_fields_absent_when_ejudge_row_missing(self):
        # pr_id set but the ejudge row is not found.
        request = FakeRequest('42')
        result = self._call(
            request,
            problem=make_problem(),
            ejudge=None,
            caps={'local/pynformatics:problem_admin': True},
        )

        for hidden in ('ejudge_contest_id', 'short_id', 'judges_settings'):
            self.assertNotIn(hidden, result)

    def test_judges_settings_parsed_and_enriched(self):
        request = FakeRequest('42')
        raw = ('[{"judge_id": 2, "contest_id": 500, "problem_id": 6, '
               '"lang_ids": [27], "user_ids": null}]')
        result = self._call(
            request,
            problem=make_problem(),
            ejudge=make_ejudge(judges_settings=raw),
            caps={'local/pynformatics:problem_admin': True},
        )

        self.assertEqual(result['judges_settings'], [{
            'judge_id': 2,
            # no rmatics.endpoint in settings, so name/url resolve to None
            'judge_name': None,
            'url': None,
            'contest_id': 500,
            'problem_id': 6,
            'lang_ids': [27],
            'user_ids': None,
        }])
        # with per-judge routing the default ejudge_contest_id is omitted
        self.assertNotIn('ejudge_contest_id', result)

    def test_judge_name_resolved_from_rmatics_endpoint(self):
        endpoint = 'http://rmatics.test'
        # avoid a stale cache entry for this endpoint between runs
        problem_view._judges_config_cache.pop(endpoint, None)

        fake_resp = mock.Mock()
        fake_resp.raise_for_status.return_value = None
        fake_resp.json.return_value = {
            'data': {'2': {'url': 'http://j2', 'name': 'Judge-2'}}
        }

        request = FakeRequest('42', settings={'rmatics.endpoint': endpoint})
        with mock.patch.object(problem_view.requests, 'get',
                               return_value=fake_resp) as get:
            result = self._call(
                request,
                problem=make_problem(),
                ejudge=make_ejudge(judges_settings='[{"judge_id": 2, "contest_id": 500, "problem_id": 6}]'),
                caps={'local/pynformatics:problem_admin': True},
            )
        self.addCleanup(problem_view._judges_config_cache.pop, endpoint, None)

        get.assert_called_once_with('{}/judges'.format(endpoint), timeout=5)
        self.assertEqual(result['judges_settings'][0]['judge_name'], 'Judge-2')
        # url is a ready-to-use ejudge master link built on the server
        self.assertEqual(result['judges_settings'][0]['url'],
                         'http://j2?contest_id=500&prob_id=6')
        # judges_settings present -> default ejudge_contest_id is not exposed
        self.assertNotIn('ejudge_contest_id', result)

    def test_judges_config_cached_for_an_hour(self):
        endpoint = 'http://rmatics.cache-test'
        problem_view._judges_config_cache.pop(endpoint, None)
        self.addCleanup(problem_view._judges_config_cache.pop, endpoint, None)

        fake_resp = mock.Mock()
        fake_resp.raise_for_status.return_value = None
        fake_resp.json.return_value = {
            'data': {'2': {'url': 'http://j2', 'name': 'Judge-2'}}
        }

        with mock.patch.object(problem_view.requests, 'get',
                               return_value=fake_resp) as get:
            problem_view._load_judges_config(endpoint)
            problem_view._load_judges_config(endpoint)

        # second call within the TTL is served from cache, not re-fetched
        get.assert_called_once()

    def test_analysis_fields_with_view_analysis_capability(self):
        request = FakeRequest('42')
        result = self._call(
            request,
            problem=make_problem(),
            caps={'local/pynformatics:problem_view_analysis': True},
        )

        self.assertEqual(result['description'], 'problem description')
        self.assertEqual(result['analysis'], 'problem analysis')
        # admin capability was not granted
        self.assertNotIn('show_limits', result)
        self.assertNotIn('sample_tests', result)

    def _languages(self, request, problem=None, user_id=7, statement=None):
        with mock.patch.object(problem_view, 'RequestGetUserId', return_value=user_id):
            return self._call(request, problem=problem or make_problem(),
                              statement=statement)['languages']

    def test_languages_from_rmatics(self):
        endpoint = 'http://rmatics.test'
        fake_resp = mock.Mock()
        fake_resp.json.return_value = {'data': [{'id': 27, 'name': 'Python 3.9'}]}
        request = FakeRequest('42', settings={'rmatics.endpoint': endpoint})
        with mock.patch.object(problem_view.requests, 'get', return_value=fake_resp) as get:
            languages = self._languages(request)

        get.assert_called_once_with('http://rmatics.test/problem/42/languages',
                                    params={'user_id': 7}, timeout=5)
        self.assertEqual(languages, [{'id': 27, 'name': 'Python 3.9'}])

    def test_output_only_language_is_named_here(self):
        fake_resp = mock.Mock()
        fake_resp.json.return_value = {'data': [{'id': 0, 'name': None}]}
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'})
        with mock.patch.object(problem_view.requests, 'get', return_value=fake_resp):
            languages = self._languages(request, problem=make_problem(output_only=True))

        self.assertEqual(languages, [{'id': 0, 'name': 'Текстовый файл'}])

    def _restricted(self, settings, params=None, **kwargs):
        """Languages 1, 3 and 27 from rmatics, narrowed by a statement."""
        fake_resp = mock.Mock()
        fake_resp.json.return_value = {'data': [
            {'id': 1, 'name': 'Free Pascal 3.0'},
            {'id': 3, 'name': 'GNU C++ 11.2'},
            {'id': 27, 'name': 'Python 3.9'},
        ]}
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'},
                              params=params or {'statement_id': '5'})
        statement = SimpleNamespace(settings=settings)
        with mock.patch.object(problem_view.requests, 'get', return_value=fake_resp):
            languages = self._languages(request, statement=statement, **kwargs)
        return [lang['id'] for lang in languages]

    def test_statement_allowed_languages_narrow_the_list(self):
        self.assertEqual(self._restricted('{"allowed_languages": [3, 71]}'), [3])

    def test_statement_without_allowed_languages_keeps_all(self):
        for settings in (None, '', '{}', '{"allowed_languages": []}',
                         '{"allowed_languages": null}'):
            self.assertEqual(self._restricted(settings), [1, 3, 27], settings)

    def test_statement_with_unreadable_settings_keeps_all(self):
        for settings in ('not json', '[1, 2]', '{"allowed_languages": 3}'):
            self.assertEqual(self._restricted(settings), [1, 3, 27], settings)

    def test_unknown_statement_keeps_all(self):
        self.assertEqual(self._restricted(None), [1, 3, 27])

    def test_missing_or_invalid_statement_id_is_ignored(self):
        settings = '{"allowed_languages": [3]}'
        self.assertEqual(self._restricted(settings, params={}), [1, 3, 27])
        self.assertEqual(self._restricted(settings, params={'statement_id': 'abc'}),
                         [1, 3, 27])

    def test_statement_narrows_the_fallback_list(self):
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'},
                              params={'statement_id': '5'})
        statement = SimpleNamespace(settings='{"allowed_languages": [27]}')
        with mock.patch.object(problem_view.requests, 'get', side_effect=OSError('down')):
            languages = self._languages(request, statement=statement)

        self.assertEqual(languages, [{'id': 27, 'name': 'Python 3.9'}])

    def test_statement_does_not_restrict_output_only(self):
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'},
                              params={'statement_id': '5'})
        statement = SimpleNamespace(settings='{"allowed_languages": [27]}')
        fake_resp = mock.Mock()
        fake_resp.json.return_value = {'data': [{'id': 0, 'name': None}]}
        with mock.patch.object(problem_view.requests, 'get', return_value=fake_resp):
            languages = self._languages(request, problem=make_problem(output_only=True),
                                        statement=statement)

        self.assertEqual(languages, [{'id': 0, 'name': 'Текстовый файл'}])

    def test_languages_fall_back_when_rmatics_is_unreachable(self):
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'})
        with mock.patch.object(problem_view.requests, 'get', side_effect=OSError('down')):
            languages = self._languages(request)

        self.assertEqual(languages, problem_view._FALLBACK_LANGUAGES)
        self.assertIn({'id': 27, 'name': 'Python 3.9'}, languages)

    def test_languages_fall_back_on_error_status(self):
        fake_resp = mock.Mock()
        fake_resp.raise_for_status.side_effect = OSError('500')
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'})
        with mock.patch.object(problem_view.requests, 'get', return_value=fake_resp):
            languages = self._languages(request)

        self.assertEqual(languages, problem_view._FALLBACK_LANGUAGES)

    def test_languages_fallback_for_output_only(self):
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'})
        with mock.patch.object(problem_view.requests, 'get', side_effect=OSError('down')):
            languages = self._languages(request, problem=make_problem(output_only=True))

        self.assertEqual(languages, [{'id': 0, 'name': 'Текстовый файл'}])

    def test_languages_fall_back_without_endpoint(self):
        self.assertEqual(self._languages(FakeRequest('42')), problem_view._FALLBACK_LANGUAGES)

    def test_not_found(self):
        request = FakeRequest('42')
        result = self._call(request, problem=None)

        self.assertEqual(request.response.status, 404)
        self.assertEqual(result, {'error': 'Problem not found'})

    def test_invalid_problem_id(self):
        request = FakeRequest('not-an-int')
        result = self._call(request, problem=make_problem())

        self.assertEqual(request.response.status, 400)
        self.assertEqual(result, {'error': 'Invalid problem id'})

    def test_internal_error_does_not_leak_details(self):
        request = FakeRequest('42')
        with mock.patch.object(problem_view, 'log') as log:
            result = self._call(request, query_raises=RuntimeError('boom'))

        self.assertEqual(request.response.status, 500)
        self.assertEqual(result, {'error': 'Internal server error'})
        # exception message / traceback must not reach the client
        self.assertNotIn('stack', result)
        self.assertNotIn('boom', str(result))
        log.exception.assert_called_once()


if __name__ == '__main__':
    unittest.main()


class ProblemSubmitsTests(unittest.TestCase):
    def _submit(self, params):
        request = FakeRequest('42', settings={'rmatics.endpoint': 'http://rmatics.test'},
                              params={'lang_id': '27', **params})
        request.POST = {'file': SimpleNamespace(file=mock.Mock())}
        resp = mock.Mock()
        resp.json.return_value = {'status': 'success'}
        with mock.patch.object(problem_view, 'RequestGetUserId', return_value=7), \
                mock.patch.object(problem_view.requests, 'post', return_value=resp) as post:
            result = problem_view.problem_submits(request)
        self.assertEqual(result, {'status': 'success'})
        return post.call_args[1]['data']

    def test_statement_id_is_passed_to_rmatics(self):
        data = self._submit({'statement_id': '5'})
        self.assertEqual(data['statement_id'], 5)
        self.assertEqual(data['lang_id'], '27')
        self.assertEqual(data['user_id'], 7)

    def test_missing_or_invalid_statement_id_is_none(self):
        self.assertIsNone(self._submit({})['statement_id'])
        self.assertIsNone(self._submit({'statement_id': 'abc'})['statement_id'])
