import traceback

import requests
from pyramid.view import view_config

from pynformatics.contest.ejudge.ejudge_proxy import rejudge
from pynformatics.utils.proxied_request_helpers import peek_request_args

from pynformatics.view.utils import *


@view_config(route_name='run.rejudge', renderer='json')
def rejudge_url(request):
    try:
        if not RequestCheckUserCapability(request, 'moodle/ejudge_submits:rejudge'):
            raise Exception('Access denied')
        contest_id = int(request.matchdict['contest_id'])
        run_id = int(request.matchdict['run_id'])
        status_id = int(request.matchdict['status_id'])
        url = request.registry.settings['ejudge.new_master_url']
        login = request.registry.settings['ejudge.master_login']
        password = request.registry.settings['ejudge.master_password']
        res = rejudge(contest_id, run_id, status_id, login, password, url)
        if (res != "ok"):
            return {"result" : "error", "message" : res}
        return {"result" : "ok"}
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


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
    url = 'http://localhost:12346/problem/run/{}'.format(run_id)
    try:
        resp = requests.put(url, json=body_params)
        return resp.json()
    except Exception as e:
        print('Request to :12346 failed!')
        print(str(e))
        return {"result": "error", "message": str(e), "stack": traceback.format_exc()}
