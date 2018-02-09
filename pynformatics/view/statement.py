from pyramid.view import view_config
from sqlalchemy import and_

from pynformatics.model.course_module import CourseModule
from pynformatics.model.statement import Statement
from pynformatics.models import DBSession
from pynformatics.utils.validators import (
    IntParam,
    validate_matchdict,
    validate_params,
)
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import StatementNotFound


@view_config(route_name='statement.get', renderer='json')
@with_context
def statement_get(request, context):
    """
    Returns statement
    """
    if not context.statement:
        raise StatementNotFound
    return context.statement.serialize(context)


@view_config(route_name='statement.set_settings', renderer='json')
@with_context(require_auth=True, require_roles='admin')
def statement_set_settings(request, context):
    context.statement.set_settings(request.json_body)
    return context.statement.serialize(context)


@view_config(route_name='statement.start_virtual', renderer='json', request_method='POST')
@validate_matchdict(IntParam('statement_id', required=True))
@with_context(require_auth=True)
def statement_start_virtual(request, context):
    password = request.json_body.get('password', '')
    participant = context.statement.start_virtual(
        user=context.user,
        password=password,
    )
    return participant.serialize(context)


@view_config(route_name='statement.finish_virtual', renderer='json', request_method='POST')
@with_context(require_auth=True)
def statement_finish_virtual(request, context):
    participant = context.statement.finish_virtual(context.user)
    return participant.serialize(context)


@view_config(route_name='statement.start', renderer='json', request_method='POST')
@validate_matchdict(IntParam('statement_id', required=True))
@with_context(require_auth=True)
def statement_start(request, context):
    password = request.json_body.get('password', '')
    participant = context.statement.start(
        user=context.user,
        password=password,
    )
    return participant.serialize(context)


@view_config(route_name='statement.finish', renderer='json', request_method='POST')
@with_context(require_auth=True)
def statement_finish(request, context):
    participant = context.statement.finish(context.user)
    return participant.serialize(context)


@view_config(route_name='statement.get_by_course_module', renderer='json', request_method='GET')
@validate_params(IntParam('course_module_id', required=True))
def statement_get_by_module(request):
    course_module_id = int(request.params['course_module_id'])
    course_module = DBSession.query(CourseModule).filter(and_(
        CourseModule.id == course_module_id,
        CourseModule.module == 19
    )).first()

    if not course_module:
        raise StatementNotFound

    request.matchdict = {'statement_id': course_module.instance}
    return statement_get(request)
