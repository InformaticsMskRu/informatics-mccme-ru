from pyramid.view import view_config

from pynformatics.utils.context import with_context


@view_config(route_name='bootstrap', renderer='json', request_method='GET')
@with_context
def bootstrap(request, context):
    serialized = {}
    if context.user:
        serialized['user'] = context.user.serialize(context)
    return serialized
