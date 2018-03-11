import logging
from pyramid.view import view_config

from pynformatics.utils.context import with_context
from pynformatics.utils.logging import db_log

log = logging.getLogger(__name__)


@view_config(route_name='bootstrap', renderer='json', request_method='GET')
@with_context
def bootstrap(request, context):
    db_log('access to bootstrap', user=context.user, instance_id=1337)
    serialized = {}
    if context.user:
        serialized['user'] = context.user.serialize(context)
    return serialized
