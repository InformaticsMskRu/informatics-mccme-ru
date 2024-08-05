from pynformatics.utils.check_role import check_global_role, is_admin 
from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Ideal, Problem, EjudgeProblem, Hint, Recommendation, SimpleUser
import sys, traceback
from phpserialize import *
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload
from sqlalchemy import desc
from pyramid.httpexceptions import HTTPFound
import sqlalchemy.orm.exc


@view_config(route_name='recommendation.get', request_method='GET', renderer='json')
@view_config(route_name='recommendation.get_html', request_method='GET', renderer='pynformatics:templates/recommendation.mak')
def get_recommedation(request):
    try:
        user_id = RequestGetUserId(request)
        try:
            user = DBSession.query(SimpleUser).filter(SimpleUser.id==user_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return {"result": "error", "error": "Not logged in"}
        if user is None:
            return {"result": "error", "error": "No such user"}
        ejuser_id = user.ejudge_id



        runs = DBSession.query(Run).filter(Run.user_id==ejuser_id).filter(Run.status==0).order_by(desc(Run.create_time)).all()

        last_run = runs[0]
        contest_id = last_run.contest_id
        problem_id = last_run.prob_id

        resolved_problems = set()
        for run in runs:
            resolved_problems.add((run.contest_id, run.prob_id))

        recommendations_row = DBSession.query(Recommendation).filter(Recommendation.contest_id==contest_id).filter(Recommendation.problem_id==problem_id).all()
        rec_result = []
        for recom in recommendations_row:
            if (recom.recommended_contest_id, recom.recommended_problem_id) not in resolved_problems:
                ej_problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.ejudge_contest_id == recom.recommended_contest_id).filter(EjudgeProblem.problem_id == recom.recommended_problem_id).first()
                problem = DBSession.query(Problem).filter(Problem.pr_id == ej_problem.ejudge_prid).first()
                rec_result.append([problem.id, problem.name])

        if len(rec_result) == 0:
            return {"result": "ok"}
        else:
            return {"result": "ok", "recommendations": rec_result}
    except Exception as e:
        return {"result" : "error", "error" : e.__str__(), "stack" : traceback.format_exc()}
