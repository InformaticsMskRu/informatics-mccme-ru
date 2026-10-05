"""Token-authorized API for submitting solutions on behalf of users.

A token (see utils/api_token.py) may submit as several users. Every run it
creates is stamped with the token's context_source, and the status endpoint
only shows runs of that context.
"""
import logging

import requests
from pyramid.response import Response
from pyramid.view import view_config

from pynformatics.utils.api_token import authenticate, error_response

log = logging.getLogger(__name__)

REQUEST_TIMEOUT = 10  # seconds


def _int_param(request, name):
    try:
        return int(request.params[name])
    except (KeyError, TypeError, ValueError):
        return None


def _rmatics_error(resp):
    """Pass an rmatics error through with its HTTP status."""
    return Response(body=resp.content, status=resp.status_code,
                    content_type='application/json')


@view_config(route_name='api.problem.submit', request_method='POST')
def api_problem_submit(request):
    token, error = authenticate(request)
    if error is not None:
        return error

    problem_id = int(request.matchdict['problem_id'])
    if not token.allows_problem(problem_id):
        return error_response(403, 'Token is not allowed to submit this problem')

    user_id = _int_param(request, 'user_id')
    if user_id is None:
        return error_response(400, 'user_id is required')
    if not token.allows_user(user_id):
        return error_response(403, 'Token is not allowed to submit as this user')

    lang_id = _int_param(request, 'lang_id')
    if lang_id is None:
        return error_response(400, 'lang_id is required')

    upload = request.POST.get('file')
    input_file = getattr(upload, 'file', None)
    if input_file is None:
        return error_response(400, 'file is required')
    input_file.seek(0)

    # statement_id and is_visible are deliberately not sent: the run belongs to
    # the token's context, not to a statement
    url = '{}/problem/trusted/{}/submit_v2'.format(
        request.registry.settings['rmatics.endpoint'], problem_id)
    data = {
        'lang_id': lang_id,
        'user_id': user_id,
        'context_source': token.context_source,
    }
    try:
        resp = requests.post(url, files={'file': input_file}, data=data,
                             timeout=REQUEST_TIMEOUT)
        content = resp.json()
    except Exception:
        log.exception('api submit: rmatics request failed, token=%s problem=%s',
                      token.id, problem_id)
        return error_response(502, 'rmatics is unavailable')

    if resp.status_code != 200 or content.get('status') != 'success':
        return _rmatics_error(resp)

    run_id = content['data']['run_id']
    log.info('api submit: token=%s user=%s problem=%s run=%s',
             token.id, user_id, problem_id, run_id)
    return Response(json_body={'run_id': run_id})


@view_config(route_name='api.run.status', request_method='GET')
def api_run_status(request):
    token, error = authenticate(request)
    if error is not None:
        return error

    run_id = int(request.matchdict['run_id'])
    url = '{}/problem/run/{}/status'.format(
        request.registry.settings['rmatics.endpoint'], run_id)
    # no user_id: rmatics then matches runs by context_source only
    params = {'is_admin': 'false', 'context_source': token.context_source}
    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        content = resp.json()
    except Exception:
        log.exception('api status: rmatics request failed, token=%s run=%s', token.id, run_id)
        return error_response(502, 'rmatics is unavailable')

    if resp.status_code != 200 or content.get('status') != 'success':
        return _rmatics_error(resp)
    return Response(json_body=content['data'])
