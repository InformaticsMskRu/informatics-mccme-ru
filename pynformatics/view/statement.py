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


@view_config(route_name='statement.start_olympiad', renderer='json', request_method='POST')
@with_context(require_auth=True)
def statement_start_olympiad(request, context):
    """
    curl -X POST http://informatics.msk.ru:6546/statement/2588/start_olympiad
    """
    return {}
