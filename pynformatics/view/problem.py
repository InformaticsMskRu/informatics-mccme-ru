import io
import json
import logging
import os
import time
import traceback
import xmlrpc.client
from urllib.parse import urlencode, urlsplit, urlunsplit

import requests
import transaction
from pyramid.view import view_config

from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.model import SimpleUser, EjudgeProblem, EjudgeProblemDummy, Problem
from pynformatics.models import DBSession
from pynformatics.utils.proxied_request_helpers import peek_request_args
from pynformatics.view.utils import *
from pynformatics.view.utils import is_authorized_id

log = logging.getLogger(__name__)

_JUDGES_CACHE_TTL_SECONDS = 60 * 60

# Cache of judges config fetched from the rmatics service, keyed by endpoint.
# Each entry is (fetched_at_monotonic, {judge_id: config_dict}).
_judges_config_cache = {}


def _load_judges_config(endpoint):
    """Fetch the judges config from the rmatics service as {judge_id: config}.

    The rmatics '/judges' endpoint returns judge routing metadata
    (name, url, lang_map) without the secret token/sender_user_id fields.
    Results are cached per endpoint for an hour; on a fetch error the last
    cached value is reused when available, otherwise an empty map is returned.
    The endpoint comes from the 'rmatics.endpoint' setting in the ini file.
    """
    if not endpoint:
        return {}

    now = time.monotonic()
    cached = _judges_config_cache.get(endpoint)
    if cached is not None and now - cached[0] < _JUDGES_CACHE_TTL_SECONDS:
        return cached[1]

    try:
        resp = requests.get('{}/judges'.format(endpoint), timeout=5)
        resp.raise_for_status()
        data = resp.json().get('data') or {}
        judges = {int(judge_id): config for judge_id, config in data.items()}
    except Exception:
        log.exception("Failed to load judges config from %s", endpoint)
        # Serve the last good value on a transient failure, but don't cache the
        # failure — the next request retries rather than waiting out the TTL.
        return cached[1] if cached is not None else {}

    _judges_config_cache[endpoint] = (now, judges)
    return judges


def _judge_config(judge_id, endpoint):
    """Return the judges config dict for a judge id, or None."""
    if judge_id is None:
        return None
    try:
        return _load_judges_config(endpoint).get(int(judge_id))
    except (TypeError, ValueError):
        return None


def _judge_name(judge_id, endpoint):
    """Return the human-readable judge name for a judges_settings entry."""
    config = _judge_config(judge_id, endpoint)
    if not config:
        return None
    return config.get('name') or None


def _judge_base_url(judge_id, endpoint):
    """Return the raw ejudge base url for a judge from the judges config."""
    config = _judge_config(judge_id, endpoint)
    if not config:
        return None
    return config.get('url') or None


def _judge_master_url(judge_id, contest_id, problem_id, endpoint):
    """Build a ready-to-use ejudge master link for a judges_settings entry.

    The client should render this url as-is, so the contest/problem query
    params are assembled here rather than on the client. Returns None when the
    judge has no url configured.
    """
    base = _judge_base_url(judge_id, endpoint)
    if not base:
        return None
    params = {}
    if contest_id is not None:
        params['contest_id'] = contest_id
    if problem_id is not None:
        params['prob_id'] = problem_id
    if not params:
        return base
    scheme, netloc, path_part, query, fragment = urlsplit(base)
    query = '&'.join(filter(None, [query, urlencode(params)]))
    return urlunsplit((scheme, netloc, path_part, query, fragment))


def _build_judges_settings(raw, endpoint):
    """Parse the mdl_ejudge_problem.judges_settings JSON and enrich each entry
    with the resolved judge name and a ready-to-use ejudge master url."""
    if not raw:
        return []
    entries = raw
    if isinstance(raw, str):
        try:
            entries = json.loads(raw)
        except ValueError:
            return []
    if not isinstance(entries, list):
        return []

    result = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        judge_id = entry.get("judge_id")
        contest_id = entry.get("contest_id")
        problem_id = entry.get("problem_id")
        result.append({
            "judge_id": judge_id,
            "judge_name": _judge_name(judge_id, endpoint),
            "url": _judge_master_url(judge_id, contest_id, problem_id, endpoint),
            "contest_id": contest_id,
            "problem_id": problem_id,
            "lang_ids": entry.get("lang_ids"),
            "user_ids": entry.get("user_ids"),
        })
    return result


def checkCapability(request, capability):
    if (not RequestCheckUserCapability(request, 'local/pynformatics:' + capability)):
        raise Exception("Auth Error")

def setShowLimits(problem_id, show_limits):
    problem = DBSession.query(Problem).filter(Problem.id == problem_id).first()

    problem.show_limits = show_limits
    with transaction.manager:
        DBSession.merge(problem)
    return "Ok"


@view_config(route_name='problem.limits.show', renderer='string')
def problem_show_limits(request):
    try:
        checkCapability(request, 'problem_edit')
        return setShowLimits(request.matchdict['problem_id'], 1)
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.get', renderer='json')
def problem_get(request):
    try:
        try:
            problem_id = int(request.matchdict['problem_id'])
        except (TypeError, ValueError):
            request.response.status = 400
            return {"error": "Invalid problem id"}

        problem = DBSession.query(Problem).filter(Problem.id == problem_id).first()
        if problem is None:
            request.response.status = 404
            return {"error": "Problem not found"}

        can_view_admin = RequestCheckUserCapability(request, 'local/pynformatics:problem_admin')
        can_view_analysis = RequestCheckUserCapability(request, 'local/pynformatics:problem_view_analysis')

        result = {
            "id": problem.id,
            "name": problem.name,
            "content": problem.content,
            "sample_tests_html": problem.sample_tests_html,
            "output_only": problem.output_only,
        }
        if problem.show_limits:
            result["timelimit"] = problem.timelimit
            result["memorylimit"] = problem.memorylimit

        # show_limits, sample_tests and the ejudge service fields require the
        # problem_admin capability
        if can_view_admin:
            result["show_limits"] = problem.show_limits
            result["sample_tests"] = problem.sample_tests

            # Query the ejudge row directly via pr_id. Querying EjudgeProblem
            # (a polymorphic subclass of Problem) by id is unreliable — it can
            # return a plain Problem without the ejudge columns.
            ejudge_problem = None
            if problem.pr_id is not None:
                ejudge_problem = DBSession.query(EjudgeProblemDummy).filter(
                    EjudgeProblemDummy.ejudge_prid == problem.pr_id).first()
            if ejudge_problem is not None:
                rmatics_endpoint = request.registry.settings.get('rmatics.endpoint')
                judges_settings = _build_judges_settings(
                    ejudge_problem.judges_settings, rmatics_endpoint)
                result["short_id"] = ejudge_problem.short_id
                result["judges_settings"] = judges_settings
                # judges_settings reroutes the problem to explicit judges, so the
                # default ejudge_contest_id no longer points at the real judge —
                # expose it only when there is no per-judge routing.
                if not judges_settings:
                    result["ejudge_contest_id"] = ejudge_problem.ejudge_contest_id

        # description and analysis require a separate capability
        if can_view_analysis:
            result["description"] = problem.description
            result["analysis"] = problem.analysis

        return result
    except Exception:
        log.exception("problem_get failed for problem_id=%s", request.matchdict.get('problem_id'))
        request.response.status = 500
        return {"error": "Internal server error"}


@view_config(route_name='problem.submit', renderer='json')
def problem_submits(request):
    # TODO: Refactor it
    user_id = RequestGetUserId(request)
    lang_id = request.params["lang_id"]
    problem_id = request.matchdict["problem_id"]
    statement_id = request.matchdict.get('statement_id')
    input_file = request.POST['file'].file

    try:
        input_file.seek(0)
        _data = {
            'lang_id': lang_id,
            'user_id': user_id,
            'statement_id': statement_id,
        }

        if "course_id" in request.params and len(request.params["course_id"]) > 0:
            course_id = int(request.params["course_id"])
            if course_id > 0:
                _data["context_source"] = CONTEXT_SHIFT + course_id

        url = '{}/problem/trusted/{}/submit_v2'.format(request.registry.settings['rmatics.endpoint'], problem_id)
        _resp = requests.post(url, files={'file': input_file}, data=_data)
        return _resp.json()
    except Exception as e:
        print(e)
        return {
            "result": "error",
            "message": e.__str__(),
            "stack": traceback.format_exc()
        }


@view_config(route_name='problem.ant.submit', renderer='json')
def problem_ant_submits(request):
    user_id = RequestGetUserId(request)
    user = DBSession.query(SimpleUser).filter(SimpleUser.id == user_id).first()
    lang_id = 67
    run_id1 = request.params["run_id1"]
    run_id2 = request.params["run_id2"]
    run_id3 = request.params["run_id3"]
    run_id4 = request.params["run_id4"]
    map_index = 0
    try:
        map_index = request.params["map_index"]
    except:
        pass
    json_names = request.params["json_names"]
    problem_id = request.matchdict["problem_id"]
    problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == problem_id).first()
    #input_file = request.POST['file'].file
    #filename = request.POST['file'].filename
    filename = "input_file.txt"
    input_file = io.StringIO("{4}${5}\n{0}\n{1}\n{2}\n{3}".format(run_id1, run_id2, run_id3, run_id4, json_names, map_index))
    ejudge_url = ""
    return {'res' : submit(input_file, problem.ejudge_contest_id, problem.problem_id, lang_id, user.login, user.password, filename, ejudge_url, user_id)}
    

@view_config(route_name='problem.tests.set_preliminary', renderer='json')
def problem_set_preliminary(request):
    try:
        checkCapability(request, 'problem_edit')
        problem = DBSession.query(Problem).filter(Problem.id == request.matchdict['problem_id']).first()

        problem.sample_tests = request.params['sample_tests']
        with transaction.manager:
           DBSession.merge(problem)
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.generate_samples', renderer='json')
def problem_generate_samples(request):
    try:
        checkCapability(request, 'problem_edit')
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        problem.generateSamples()

        with transaction.manager:
           DBSession.merge(problem)
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.limits.hide', renderer='string')
def problem_hide_limits(request):
    try:
        checkCapability(request, 'problem_edit')
        return setShowLimits(request.matchdict['problem_id'], 0)
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='problem.tests.count', renderer='string')
def problem_get_tests_count(request):
    try:
        checkCapability(request, 'problem_teacher_view')
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)
        cnt = 0
        res = ""
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            if os.path.exists(test_file_name):
                res += test_file_name
            else:
                break
        return cnt - 1
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='problem.tests.get_test', renderer='json')
def problem_get_test(request):
    try:
        checkCapability(request, 'problem_teacher_view')
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()

        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_test(test_num)}
    except Exception as e:
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.add', renderer='json')
def problem_add_test(request):
    try:
        checkCapability(request, 'problem_edit')
        s = xmlrpc.client.ServerProxy('http://localhost:7080/')

        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)

        cnt = 0
        flag = False
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            corr_file_name = (prob.tests_dir + prob.corr_pat) % cnt
            if not os.path.exists(test_file_name):
                flag = True
                break

        if flag:
            s.add_file(test_file_name, request.params['input_data'])
            s.add_file(corr_file_name, request.params['output_data'])
        return {"result" : "ok", "content" : test_file_name}
    except Exception as e:
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.get_corr', renderer='json')
def problem_get_corr(request):
    try:
        checkCapability(request, 'problem_teacher_view')
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()

        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_corr(test_num)}
    except Exception as e:
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.filter_runs', renderer='json')
def problem_runs_filter_proxy(request):
    user_id = RequestGetUserId(request)  # Returns -1 if not authorised

    if not is_authorized_id(user_id):
        return {'result': 'error', 'message': 'Not authorized'}

    problem_id = request.matchdict.get('problem_id')
    if problem_id is None:
        return {"result": "error", "message": 'Problem id required'}

    filter_params = ['user_id', 'group_id',
                     'lang_id', 'status_id', 'statement_id',
                     'count', 'page',
                     'from_timestamp', 'to_timestamp']

    params, _ = peek_request_args(request, filter_params)

    if "group_id" not in params and "statement_id" in params:
        user_ids = GetUserIds(request, params["statement_id"], 0)
    else:
        user_ids = None

    try:
        checkCapability(request, 'show_hidden_submits')
        params['show_hidden'] = True
        if request.params.get('include_source'):
            params['include_source'] = True
    except Exception as exc:
        pass

    url = '{}/problem/{}/submissions/'.format(request.registry.settings['rmatics.endpoint'], problem_id)
    try:
        if user_ids:
            resp = requests.post(url, json={"user_ids": user_ids}, params=params)
        else:
            resp = requests.get(url, params=params)
        res = resp.json()
  
        course_id = 0
        if "course_id" in request.params:
            course_id = int(request.params["course_id"]) + CONTEXT_SHIFT
        for run in res["data"]:
            if "context_source" in run and run["context_source"]:
                run["current"] = int(run["context_source"]) == course_id
                del run["context_source"]
        return res
    except (requests.RequestException, ValueError) as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}


@view_config(route_name='problem.runs.source', renderer='json')
def problem_get_run_source(request):
    run_id = request.matchdict.get('run_id')
    if run_id is None:
        return {"result": "error", "message": 'Run id required'}

    params = GetUserCourseContextParams(request, "mod/statement:view_source", "moodle/ejudge_submits:admin")

    if not params:
        return {'result': 'error', 'message': 'Not authorized'}

    try:
        url = '{}/problem/run/{}/source/'.format(request.registry.settings['rmatics.endpoint'], run_id)
        resp = requests.get(url, params=params)
        return resp.json()
    except (requests.RequestException, ValueError) as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}
