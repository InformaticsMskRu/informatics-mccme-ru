import traceback

import requests
from pyramid.view import view_config

from pynformatics.contest.ejudge.ejudge_proxy import rejudge
from pynformatics.utils.proxied_request_helpers import peek_request_args

from pynformatics.view.utils import *


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
        url = 'http://localhost:12346/problem/run/{}/action/rejudge'.format(run_id)
        request_func = requests.post
        request_kwargs = {}
    else:
        url = 'http://localhost:12346/problem/run/{}'.format(run_id)
        request_func = requests.put
        request_kwargs = {'json': body_params}

    try:
        resp = request_func(url, **request_kwargs)
        return resp.json()
    except Exception as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}
