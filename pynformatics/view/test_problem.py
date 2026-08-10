import unittest
from types import SimpleNamespace
from unittest import mock

from pynformatics.view import problem as problem_view


class FakeResponse:
    def __init__(self):
        self.status = 200


class FakeRequest:
    def __init__(self, problem_id):
        self.matchdict = {'problem_id': problem_id}
        self.response = FakeResponse()


def make_problem(**overrides):
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
    )
    attrs.update(overrides)
    # SimpleNamespace rather than Mock: Mock reserves the name kwarg for the
    # mock's own label, so problem.name would return a child mock, not the value.
    return SimpleNamespace(**attrs)


class ProblemGetTests(unittest.TestCase):
    def _call(self, request, problem=None, caps=None, query_raises=None):
        """Invoke problem_get with DBSession and capability checks mocked.

        caps maps a capability string -> bool; anything not listed is denied.
        """
        caps = caps or {}
        query = mock.Mock()
        query.filter.return_value.first.return_value = problem

        def cap_check(_request, capability, *args, **kwargs):
            return caps.get(capability, False)

        with mock.patch.object(problem_view, 'DBSession') as db, \
                mock.patch.object(problem_view, 'RequestCheckUserCapability',
                                  side_effect=cap_check):
            if query_raises is not None:
                db.query.side_effect = query_raises
            else:
                db.query.return_value = query
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
            caps={'local/pynformatics:problem_admin': True},
        )

        self.assertEqual(result['show_limits'], True)
        self.assertEqual(result['sample_tests'], '1,2')
        # analysis capability was not granted
        self.assertNotIn('description', result)
        self.assertNotIn('analysis', result)

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
