from pynformatics.utils.check_role import check_global_role, is_admin 
from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Ideal, Problem, EjudgeProblem, Run, Hint, Recommendation
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

@view_config(route_name='recommendation.get', request_method='GET', renderer='json')
@view_config(route_name='recommendation.get_html', request_method='GET', renderer='pynformatics:templates/recommendation.mak')
def get_recommedation(request):
    try:
        try:
            user_id = request.params['user_id']
        except KeyError:
            return {"result": "error", "error": "user_id is missing"}
        user = DBSession.query(User).filter_by(id=user_id).one()
        if user is None:
            return {"result": "error", "error": "No such user"}


        run = DBSession.query(Run).filter_by(user=user).filter_by(status=0).one()

        contest_id = run.contest_id
        problem_id = run.prob_id

        recommendations_row = DBSession.query(Recommendation).filter_by(contest_id=contest_id).filter_by(problem_id=problem_id).all()
        rec_result = []
        for recom in recommendations_row:
            ej_problem = DBSession.query(EjudgeProblem).filter_by(contest_id=recom.recommended_contest_id).filter_by(problem_id=recom.recommended_problem_id).first()
            problem = DBSession.query(Problem).filter(Problem.pr_id == ej_problem.ejudge_prid).first()
            rec_result.append([problem.id, problem.name])

        if len(rec_result) == 0:
            return {"result": "ok"}
        else:
            return {"result": "ok", "recommendations": rec_result}
    except Exception as e:
        return {"result" : "error", "error" : e.__str__(), "stack" : traceback.format_exc()}