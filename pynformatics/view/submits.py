from pyramid.view import view_config

from sqlalchemy import desc, asc

from pynformatics.models import DBSession
from pynformatics.model import SimpleUser, Run, Group, UserGroup, EjudgeProblem
from pynformatics.view.utils import RequestGetUserId
from pynformatics.utils.run import get_status_by_id

def get_submits_query(request):
    user_id = int(request.params.get("user_id", RequestGetUserId(request)))
    limit = int(request.params.get("limit", 1000))
    offset = int(request.params.get("offset", 0))

    query = DBSession.query(Run, SimpleUser, EjudgeProblem)\
    .join(SimpleUser, SimpleUser.ejudge_id == Run.user_id)\
    .join(EjudgeProblem, EjudgeProblem.ejudge_contest_id == Run.contest_id)\
    .filter(EjudgeProblem.problem_id == Run.prob_id)\
    .filter(SimpleUser.id == user_id)\
    .order_by(desc(Run.create_time))
    return query
    

@view_config(route_name='submits.get', renderer='pynformatics:templates/submits.mak')
#@view_config(route_name='submits.get', renderer='json')
def submits_user_get(request):
    query = get_submits_query(request)
    result_list = list()
    for run, simple_user, ej_problem in query.all():
        result_list.append(
            {"contest_id": run.contest_id, 
            "problem_id": run.prob_id,
            "problem_name": ej_problem.name.strip(),
            "user": "{0} {1}".format(simple_user.firstname, simple_user.lastname),
            "status": get_status_by_id(run.status),
            "date": run.create_time,
            "test_num": run.test_num,
            "score": run.score})
    return {"query": str(query), "submits":result_list}