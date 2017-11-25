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
from pyramid.httpexceptions import HTTPFound


def get_test_signature(run):
    run.fetch_tested_protocol_data()
    return ''.join(test[1]['status'] for test in sorted(run.tests.items(), key=lambda x:int(x[0])))
    
def get_run_code(run_id, contest_id):
    run_id = int(run_id)
    tmp_id = int(run_id//32)
    contest_id = int(contest_id)
    
    d3 = tmp_id % 32
    tmp_id = tmp_id // 32
    
    d2 = tmp_id % 32
    tmp_id = tmp_id // 32

    d1 = tmp_id % 32
    tmp_id = tmp_id // 32
    
    if d1 > 9:
        d1 = chr(ord('A') + d1 - 10)
    
    if d2 > 9:
        d2 = chr(ord('A') + d2 - 10)

    if d3 > 9:
        d3 = chr(ord('A') + d3 - 10)

    contest_id = str(contest_id)
    while len(contest_id)<6:
        contest_id = '0' + contest_id

    run_id = str(run_id)
    while len(run_id)<6:
        run_id = '0' + run_id

    path = '/home/judges/' + contest_id + '/var/archive/runs/' + str(d1) + '/' + str(d2) + '/' + str(d3) + '/' + run_id
    codefile = open(path, encoding='utf-8')
    code = codefile.read()
    codefile.close()
    return code


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
        
@view_config(route_name='hint.get_run', request_method='GET', renderer='json')
@check_global_role("admin")
def get_run(request):
    try:
        try:
            contest_id = request.params['contest_id']
            run_id = request.params['run_id']
        except KeyError:
            return {"result": "error", "error": "run_id or contest_id is missing"}
        run = Run.get_by(run_id, contest_id)
        if run is None:
            return {"result": "error", "error": "No such run"}
        moodle_pid = DBSession.query(Problem).filter(Problem.pr_id == run.problem.ejudge_prid).first().id
        return {"result": "ok", "contest_id": run.contest_id, "problem_id": run.prob_id, "moodle_problem_id": moodle_pid,
                "signature": get_test_signature(run), "code": get_run_code(run_id, contest_id)} 
    except Exception as e:
        return {"result" : "error", "error" : e.__str__(), "stack" : traceback.format_exc()}
        
@view_config(route_name='hint.add_page', request_method='GET', renderer='pynformatics:templates/addhint.mak')
def add_page(request):
    return {}


@view_config(route_name='hint.delete', request_method='POST', renderer='json')
@check_global_role("admin")
def delete(request):
    try:
        hint_id = request.params['id']
        if DBSession.query(Hint).filter(Hint.id == hint_id).delete():
            return {"result": "ok"}
        else:
            return {"result": "error", "error": "no such hint"}
    except Exception as e:
        return {"result" : "error", "error" : e.__str__(), "stack" : traceback.format_exc()}

    
@view_config(route_name='hint.get_by_problem', request_method='GET', renderer='json')
@view_config(route_name='hint.get_by_problem_html', request_method='GET', renderer='pynformatics:templates/hints_by_problem.mak')
@check_global_role("admin")
def get_by_problem(request):
    try:
        try:
            problem_id = request.params['problem_id']
        except KeyError:
            return {"result": "error", "error": "problem_id is missing"}
        hints = DBSession.query(Hint, Problem, EjudgeProblem).filter(Problem.id == problem_id).filter(EjudgeProblem.ejudge_prid == Problem.pr_id)\
                  .filter(Hint.contest_id == EjudgeProblem.ejudge_contest_id).filter(Hint.problem_id == EjudgeProblem.problem_id).all()
        hints = [[hint[0].id, hint[0].test_signature, hint[0].comment] for hint in hints]
        return {"result": "ok", "hints": hints}
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