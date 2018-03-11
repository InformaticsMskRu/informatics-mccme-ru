from pyramid.view import view_config
from sqlalchemy.orm.exc import NoResultFound

from pynformatics import DBSession
from pynformatics.model import GroupInviteLink, Group, UserGroup
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import BadRequest, NotFound
from pynformatics.utils.url_generator import IntUrlGenerator
from pynformatics.utils.validators import Param, validate_matchdict


@view_config(route_name='invite.get', renderer='json', request_method='GET')
@with_context(require_auth=True)
@validate_matchdict(Param('link', required=True))
def invite_get(request, context, *, link):
    user_id = context.user.id
    invite_id = IntUrlGenerator().decode(link)
    invite: GroupInviteLink = DBSession.query(GroupInviteLink).get(invite_id)
    if not invite:
        raise NotFound("This invite doesn't exist")
    if not invite.is_active:
        raise BadRequest("This invite is not active anymore")
    group = DBSession.query(Group).get(invite.group_id)
    DBSession.add(
        UserGroup(user_id=user_id, group_id=group.id)
    )
    DBSession.flush()
    try:
        redirect = invite.get_redirect(DBSession)
    except NoResultFound:
        raise BadRequest("Can't find {} with id {}".format(invite.redirect_type, invite.redirect_id))
    return {
        'redirect': {
            'type': invite.redirect_type, 'id': invite.redirect_id
        } if redirect else None,
        'group': group.serialize()
    }

