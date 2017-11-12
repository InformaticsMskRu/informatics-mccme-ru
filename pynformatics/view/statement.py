from pyramid.view import view_config

from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import StatementNotFound


@view_config(route_name='statement.get', renderer='json')
@with_context
def statement_get(request, context):
    """
    curl -v http://informatics.msk.ru:6546/statement/2588
    """
    if not context.statement:
        raise StatementNotFound
    attrs = [
        'course',
        'name',
        'settings',
    ]
    statement_dict = {
        attr: getattr(context.statement, attr)
        for attr in attrs
    }
    statement_dict['problems'] = {
        rank: statement_problem.problem.id
        for rank, statement_problem in context.statement.StatementProblems.items()
        if not statement_problem.hidden
    }
    return statement_dict
