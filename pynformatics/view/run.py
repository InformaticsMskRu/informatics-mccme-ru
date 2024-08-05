import traceback

import requests
from pyramid.view import view_config

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
