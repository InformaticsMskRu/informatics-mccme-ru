import traceback

from pyramid.view import view_config

from pynformatics.contest.ejudge.ejudge_proxy import rejudge

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
