from pynformatics.utils.check_role import check_global_role, is_admin 
from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Ideal, Problem, EjudgeProblem
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

def get_ok_runs(user_id, problem_id):
    user = DBSession.query(User).filter_by(id=user_id).one()
    problem = DBSession.query(EjudgeProblem).filter_by(id=problem_id).one()
    user_ejudge_id = user.ejudge_id
    pr_id = problem.problem_id
    contest_id = problem.ejudge_contest_id

    ok_runs = DBSession.query(Run).filter_by(user_id=user_ejudge_id,
        prob_id=pr_id, contest_id=contest_id, status=0).all()
    ac_runs = DBSession.query(Run).filter_by(user_id=user_ejudge_id,
        prob_id=pr_id, contest_id=contest_id, status=8).all()
    return ok_runs + ac_runs

@view_config(route_name='ideal.add', request_method='POST', renderer='json')
def add(request):
    try:
        author_id = RequestGetUserId(request) # TODO: 0 - not logged in, 1 - guest
        problem_id = int(html.escape(request.params['problem_id'])) 
        contest_id = int(html.escape(request.params['contest_id'])) 
        run_id = int(html.escape(request.params['run_id'])) 
        comment = html.escape(request.params.get('comment', '')) 
        if is_admin(request):
            status = 1
        else:
            status = 0
        ideal = Ideal(problem_id, run_id, contest_id, author_id, comment, status)
        with transaction.manager:
            DBSession.add(ideal)
        return HTTPFound(location="/mod/statements/view3.php?chapterid=" + str(problem_id))
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='ideal.add_form', request_method='GET', renderer='pynformatics:templates/ideal_add_form.mak')
def add_form(request):
    try:
        problem_id = int(html.escape(request.params['problem_id'])) 
        run_id = int(html.escape(request.params['run_id'])) 
        contest_id = int(html.escape(request.params['contest_id'])) 
        return {"problem_id": problem_id, "run_id":run_id, "contest_id":contest_id}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='ideal.approve', request_method='GET', renderer='json')
@check_global_role("admin")
def approve(request):
    try:
        id = int(html.escape(request.params['id'])) 
        ideal = DBSession.query(Ideal).filter_by(id=id).first()
        ideal.status = html.escape(request.params['status']) 
        with transaction.manager:
            DBSession.merge(ideal)
        return HTTPFound(location="/mod/statements/view3.php?chapterid=" + str(ideal.problem_id))
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='ideal.get_by_problem', request_method='GET', renderer='json')
@view_config(route_name='ideal.get_by_problem_html', request_method='POST', renderer='pynformatics:templates/ideal_list.mak')
def get_by_problem(request):
    try:
        user_id = int(RequestGetUserId(request)) # TODO: 0 - not logged in, 1 - guest
        problem_id = html.escape(request.params['problem_id']) 
        ok_runs = get_ok_runs(user_id, problem_id)
        ideals = DBSession.query(Ideal).filter_by(problem_id=problem_id).filter_by(status=1).all()
        future_ideals = DBSession.query(Ideal).filter_by(problem_id=problem_id).filter_by(status=0).all()
        return {"result": "ok", "ideals":ideals, "future_ideals":future_ideals, "problem_id": problem_id, "ok_runs": ok_runs, 'is_admin': is_admin(request)}
    except Exception as e: 
        return {"result": "error", "message": e.__str__(), "stack": traceback.format_exc()}

@view_config(route_name='ideal.suggested', request_method='GET', renderer='json')
@view_config(route_name='ideal.suggested_html', request_method='GET', renderer='pynformatics:templates/ideal_suggest.mak')
def get_suggested(request):
    try:
        suggested = DBSession.query(Ideal).filter_by(status=0).all()
        problems = sorted(list(set(suggest.problem_id for suggest in suggested)))
        return {"result": "ok", "problems": problems, 'suggested':suggested}
    except Exception as e: 
        return {"result": "error", "message": e.__str__(), "stack": traceback.format_exc()}

