# import json

# from pyramid.view import view_config

# from sqlalchemy import desc, asc

# from pynformatics.models import DBSession
# from pynformatics.model import SimpleUser, EjudgeRun, Group, UserGroup, EjudgeProblem, UserGroup
# from pynformatics.view.utils import RequestGetUserId
# from pynformatics.utils.run import get_status_by_id, get_lang_name_by_id

# class SubmitQueryParams:
#     def __init__(self, request):
#         self.user_id = request.params.get("user_id", None)
#         if self.user_id is not None:
#             self.user_id = int(self.user_id)

#         self.problem_id = request.params.get("problem_id", None)
#         if self.problem_id is not None:
#             self.problem_id = int(self.problem_id)

#         self.contest_id = request.params.get("contest_id", None)
#         if self.contest_id is not None:
#             self.contest_id = int(self.contest_id)

#         self.group_id = request.params.get("group_id", None)
#         if self.group_id is not None:
#             self.group_id = int(self.group_id)

#         self.limit = int(request.params.get("limit", 10))
#         self.offset = int(request.params.get("offset", 0))



# def get_submits_query(params):

#     query = DBSession.query(EjudgeRun, SimpleUser, EjudgeProblem)\
#     .join(SimpleUser, SimpleUser.ejudge_id == EjudgeRun.user_id)\
#     .join(EjudgeProblem, (EjudgeProblem.ejudge_contest_id == EjudgeRun.contest_id) & (EjudgeProblem.problem_id == EjudgeRun.prob_id))
    
#     if params.group_id is not None:
#         query = query.join(UserGroup, SimpleUser.id == UserGroup.user_id).filter(UserGroup.group_id == params.group_id)

#     if params.user_id is not None:
#         query = query.filter(SimpleUser.id == params.user_id)
    
#     if params.problem_id is not None:
#         query = query.filter(EjudgeProblem.id == params.problem_id)

    
#     query = query.order_by(desc(EjudgeRun.create_time))
#     query = query.slice(params.offset, params.offset + params.limit)

#     return query
    

# @view_config(route_name='submits.get', renderer='pynformatics:templates/submits.mak')
# #@view_config(route_name='submits.get', renderer='json')
# def submits_user_get(request):
#     request_params = SubmitQueryParams(request)
#     query = get_submits_query(request_params)
#     result_list = list()
#     for run, simple_user, ej_problem in query.all(): 
#         result_list.append(
#             {"contest_id": run.contest_id, 
#             "problem_id": run.prob_id,
#             "ejudge_prid": ej_problem.ejudge_prid,
#             "problem_name": ej_problem.name.strip(),
#             "user": "{0} {1}".format(simple_user.firstname, simple_user.lastname),
#             "status": get_status_by_id(run.status),
#             "date": run.create_time,
#             "lang_name": get_lang_name_by_id(run.lang_id),
#             "test_num": run.test_num,
#             "score": run.score})
#     return {"query": str(query), "count": query.count(), "submits":result_list, "request_params":request_params.__dict__}