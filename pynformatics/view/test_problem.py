import json
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

from pynformatics.view import problem as problem_view


class FakeResponse:
    def __init__(self):
        self.status = 200


class FakeRequest:
    def __init__(self, problem_id, settings=None):
        self.matchdict = {'problem_id': problem_id}
        self.response = FakeResponse()
        self.registry = SimpleNamespace(settings=settings or {})


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
    def _call(self, request, problem=None, ejudge=None, caps=None, query_raises=None):
        """Invoke problem_get with DBSession and capability checks mocked.

        The base Problem query returns `problem`; the EjudgeProblemDummy query
        returns `ejudge`. caps maps a capability string -> bool; anything not
        listed is denied.
        """
        caps = caps or {}

        def query_for(model):
            query = mock.Mock()
            if model is problem_view.EjudgeProblemDummy:
                query.filter.return_value.first.return_value = ejudge
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
            # no judges.config_path in settings, so name/url resolve to None
            'judge_name': None,
            'url': None,
            'contest_id': 500,
            'problem_id': 6,
            'lang_ids': [27],
            'user_ids': None,
        }])
        # with per-judge routing the default ejudge_contest_id is omitted
        self.assertNotIn('ejudge_contest_id', result)

    def test_judge_name_resolved_from_config_path_setting(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as config_file:
            json.dump({'2': {'url': 'http://j2', 'name': 'Judge-2'}}, config_file)
            config_path = config_file.name
        self.addCleanup(os.unlink, config_path)
        # avoid a stale cache entry for this path between runs
        problem_view._judges_config_cache.pop(config_path, None)

        request = FakeRequest('42', settings={'judges.config_path': config_path})
        result = self._call(
            request,
            problem=make_problem(),
            ejudge=make_ejudge(judges_settings='[{"judge_id": 2, "contest_id": 500, "problem_id": 6}]'),
            caps={'local/pynformatics:problem_admin': True},
        )

        self.assertEqual(result['judges_settings'][0]['judge_name'], 'Judge-2')
        # url is a ready-to-use ejudge master link built on the server
        self.assertEqual(result['judges_settings'][0]['url'],
                         'http://j2?contest_id=500&prob_id=6')
        # judges_settings present -> default ejudge_contest_id is not exposed
        self.assertNotIn('ejudge_contest_id', result)

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
