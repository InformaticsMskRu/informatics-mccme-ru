from pyramid.view import view_config

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
