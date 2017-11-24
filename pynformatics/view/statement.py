from pyramid.view import view_config

from pynformatics.utils.check_role import check_global_role
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
@check_global_role(('admin'))
@with_context(require_auth=True)
def statement_set_settings(request, context):
    return context.statement.set_settings(request.json_body)


@view_config(route_name='statement.start_virtual', renderer='json', request_method='POST')
@with_context(require_auth=True)
def statement_start_virtual(request, context):
    new_virtual_participant = context.statement.start_virtual(context.user)
    return new_virtual_participant.serialize(context)


@view_config(route_name='statement.finish_virtual', renderer='json', request_method='POST')
@with_context(require_auth=True)
def statement_finish_virtual(request, context):
    virtual_participant = context.statement.finish_virtual(context.user)
    return virtual_participant.serialize(context)
