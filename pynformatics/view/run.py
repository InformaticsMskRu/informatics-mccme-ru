import logging
import traceback

import requests
from pyramid.response import Response
from pyramid.view import view_config

from pynformatics.utils.proxied_request_helpers import peek_request_args

from pynformatics.view.utils import *

log = logging.getLogger(__name__)

REQUEST_TIMEOUT = 5  # seconds


@view_config(route_name='problem.runs.update', renderer='json')
def update_run(request):
    """ Proxy View for core::problem/run/<run_id> """
    try:
        if not RequestCheckUserCapability(request, 'moodle/ejudge_submits:rejudge'):
            raise Exception('Access denied')
    except Exception as e:
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

    run_id = request.matchdict['run_id']
    update_params = ['ejudge_status']
    _, body_params = peek_request_args(request, post_params=update_params)

    new_status = body_params.get('ejudge_status')

    # 99 is Перетестировать
    if new_status and int(new_status) == 99:
        url = '{}/problem/run/{}/action/rejudge'.format(request.registry.settings['rmatics.endpoint'], run_id)
        request_func = requests.post
        request_kwargs = {}
    else:
        url = '{}/problem/run/{}'.format(request.registry.settings['rmatics.endpoint'], run_id)
        request_func = requests.put
        request_kwargs = {'json': body_params}

    try:
        resp = request_func(url, **request_kwargs)
        return resp.json()
    except Exception as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}


@view_config(route_name='problem.runs.status', renderer='json')
def get_run_status(request):
    """ Proxy View for core::problem/run/<run_id>/status
    {"ejudge_status": <int>, "ejudge_score": <int|null>,
     "ejudge_test_num": <int|null>}
    ejudge_score/ejudge_test_num = null, пока посылка не оттестирована.
    """
    params = GetUserCourseContextParams(request,
                                        "mod/statement:view_protocol",
                                        "moodle/ejudge_submits:admin")

    if not params:
        return {'result': 'error', 'message': 'Not authorized'}

    run_id = int(request.matchdict['run_id'])
    url = '{}/problem/run/{}/status'.format(
        request.registry.settings['rmatics.endpoint'], run_id)

    try:
        resp = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        content = resp.json()
    except Exception:
        log.exception("Failed to get run status from rmatics for run_id=%s", run_id)
        request.response.status = 500
        return {'result': 'error', 'message': 'Internal server error'}
    
    if content.get('status') != 'success':
        return content

    return content['data']


@view_config(route_name='problem.runs.update_from_ejudge_v2', request_method='POST')
def update_run_from_ejudge_v2(request):
    """ Proxy View for core::problem/run/action/update_from_ejudge_v2

    Called by notify-worker on judge nodes. Authorization is the judge's
    Bearer token, checked by rmatics, so the header and body are forwarded
    as is and the rmatics status code is returned unchanged: notify-worker
    relies on it to detect a rejected notification.
    """
    url = '{}/problem/run/action/update_from_ejudge_v2'.format(
        request.registry.settings['rmatics.endpoint'])

    if request.content_type != 'application/json':
        return Response(status=400)
    if 'Authorization' not in request.headers:
        return Response(status=403)

    headers = {'Content-Type': request.content_type,
               'Authorization': request.headers['Authorization']}

    try:
        resp = requests.post(url, data=request.body, headers=headers,
                             timeout=REQUEST_TIMEOUT)
    except Exception:
        log.exception("Failed to forward ejudge notification to rmatics")
        return Response(json_body={'result': 'error', 'message': 'rmatics is unavailable'},
                        status=502)

    response = Response(body=resp.content, status=resp.status_code)
    response.headers['Content-Type'] = resp.headers.get('Content-Type', 'application/json')
    return response
