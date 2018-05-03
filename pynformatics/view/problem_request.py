import transaction
from pyramid.view import view_config

from pynformatics import DBSession, EjudgeProblem
from pynformatics.model.problem_request import ProblemRequest, ProblemRequestStatus
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import ProblemRequestNotFound, ProblemNotFound, ProblemRequestNoChanges, \
    ProblemRequestAlreadyReviewed


@view_config(route_name='problem_request.create', renderer='json', request_method='POST')
@with_context(require_auth=True)
def create_problem_request(request, context):
    problem_id = int(request.json_body.get('problem_id'))
    problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == problem_id).first()

    if not problem:
        raise ProblemNotFound

    user_id = context.user_id
    name = request.json_body.get('name')
    content = request.json_body.get('content')

    if problem.name == name and problem.content == content:
        raise ProblemRequestNoChanges

    problem_request = ProblemRequest(problem_id, user_id, name, content)

    DBSession.add(problem_request)
    transaction.commit()
    return {'result': 'ok'}


@view_config(route_name='problem_requests.get', renderer='json')
@with_context(require_auth=True, require_roles='admin')
#@with_context
def problem_requests_get(request, context):
    problem_requests = DBSession.query(ProblemRequest)
    return [problem_request.serialize(context) for problem_request in problem_requests]


@view_config(route_name='problem_request.get', renderer='json')
@with_context(require_auth=True, require_roles='admin')
#@with_context
def problem_request_get(request, context):
    problem_request_id = int(request.matchdict['problem_request_id'])
    problem_request = DBSession.query(ProblemRequest).filter(ProblemRequest.id == problem_request_id).first()
    if not problem_request:
        raise ProblemRequestNotFound
    return problem_request.serialize(context)


@view_config(route_name='problem_request_decline', renderer='json', request_method='POST')
@with_context(require_auth=True, require_roles='admin')
#@with_context
def problem_request_decline(request, context):
    problem_request_id = int(request.json_body.get('problem_request_id'))
    problem_request = DBSession.query(ProblemRequest).filter(ProblemRequest.id == problem_request_id).first()

    if not problem_request:
        raise ProblemRequestNotFound

    if problem_request.status != ProblemRequestStatus.REVIEW.value:
        raise ProblemRequestAlreadyReviewed

    problem_request.status = ProblemRequestStatus.DECLINED.value

    DBSession.merge(problem_request)
    transaction.commit()
    return {'result': 'ok'}


@view_config(route_name='problem_request_approve', renderer='json', request_method='POST')
@with_context(require_auth=True, require_roles='admin')
#@with_context
def problem_request_approve(request, context):
    problem_request_id = int(request.json_body.get('problem_request_id'))
    problem_request = DBSession.query(ProblemRequest).filter(
        ProblemRequest.id == problem_request_id).first()

    if not problem_request:
        raise ProblemRequestNotFound

    name = request.json_body.get('name') or problem_request.name
    content = request.json_body.get('content') or problem_request.content

    if problem_request.status != ProblemRequestStatus.REVIEW.value:
        raise ProblemRequestAlreadyReviewed

    problem = problem_request.get_problem()

    if problem.name == name and problem.content == content:
        raise ProblemRequestNoChanges

    problem_request.status = ProblemRequestStatus.APPROVED.value
    problem.name = problem_request.name
    problem.content = problem_request.content


    DBSession.merge(problem_request)
    #DBSession.merge(problem)

    transaction.commit()
    return {'result': 'ok'}
