from pyramid.view import view_config

from pynformatics.contest.ejudge.submit_queue import peek_user_submits
from pynformatics.utils.context import with_context
from pynformatics.utils.validators import (
    IntParam,
    validate_params,
)


@view_config(route_name='submit.get', renderer='json', request_method='GET')
@with_context(require_auth=True)
def submit_get(request, context):
    submits = peek_user_submits(user_id=context.user_id)
    return [
        submit.serialize(context)
        for submit in submits
    ]
    
