from pyramid.view import view_config

from pynformatics.model.group_invite import GroupInvite
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context



@view_config(route_name='group_invite.get', renderer='json', request_method='GET')
@with_context(require_auth=True)
def group_invite_get(request, context):
    group_invites = DBSession.query(GroupInvite).filter_by(creator_id=context.user_id).all()
    return [
        group_invite.serialize(context)
        for group_invite in group_invites
    ]
