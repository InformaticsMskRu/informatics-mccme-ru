from pynformatics.utils.check_role import check_global_role, is_admin 
from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Ideal, Problem, EjudgeProblem, Run, Hint
import sys, traceback
from phpserialize import *
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload
from pyramid.security import authenticated_userid
from pyramid.httpexceptions import HTTPFound


def get_test_signature(run):
    run.tested_protocol  # magic
    return ''.join(test[1]['status'] for test in sorted(run.tests.items(), key=lambda x:int(x[0])))


@view_config(route_name='hint.get', request_method='GET', renderer='json')
@view_config(route_name='hint.get_html', request_method='GET', renderer='pynformatics:templates/hint.mak')
def get_hint(request):
    try:
        try:
            contest_id = request.params['contest_id']
            run_id = request.params['run_id']
        except KeyError:
            return {"result": "error", "error": "run_id or contest_id is missing"}
        run = Run.get_by(run_id, contest_id)
        if run is None:
            return {"result": "error", "error": "No such run"}
        author_id = run.user.firstname + ' ' + run.user.lastname
        problem_id = run.problem.ejudge_prid
        problem_name = DBSession.query(Problem).filter(Problem.pr_id == problem_id).first().name
        signature = get_test_signature(run)
        if signature == 'SE' * (len(signature) // 2):
            hint = Hint.get_by(0, 0, 0, 'SE')
        else:
            hint = Hint.get_by(contest_id, run.prob_id, run.lang_id, signature)
        if hint is None:
            return {"result": "ok", "user_name" : author_id, "problem_name" : problem_name}
        return {"result": "ok", "hint" : hint.comment, "user_name" : author_id, "problem_name" : problem_name}
    except Exception as e:
        return {"result" : "error", "error" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='hint.add', request_method='POST', renderer='json')
@check_global_role("admin")
def add_hint(request):
    try:
        problem_id = int(html.escape(request.params['problem_id'])) 
        contest_id = int(html.escape(request.params['contest_id']))
        signature = html.escape(request.params['signature'])
        comment = html.escape(request.params['comment']) 
        hint = Hint(problem_id, contest_id, 0, signature, comment)
        with transaction.manager:
            DBSession.add(hint)
        return {"result" : "ok"}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}