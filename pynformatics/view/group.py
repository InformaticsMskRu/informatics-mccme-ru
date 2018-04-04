from pyramid.view import view_config
from sqlalchemy import and_

from pynformatics.model.group import (
    Group,
    UserGroup,
)
from pynformatics.model.group_invite import GroupInvite
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import GroupNotFound
from pynformatics.utils.validators import (
    IntParam,
    Param,
    validate_matchdict,
    validate_params,
)


@view_config(route_name='group.get', renderer='json', request_method='GET')
@validate_matchdict(IntParam('group_id', required=True))
@with_context
def group_get(request, context):
    group_id = int(request.matchdict['group_id'])
    try:
        group = DBSession.query(Group).filter(
            and_(
                Group.id == group_id,
                Group.visible == True
            )
        ).one()
    except Exception:
        raise GroupNotFound

    return group.serialize(context)


@view_config(route_name='group.search', renderer='json', request_method='GET')
@validate_params(Param('name'))
@with_context
def group_search(request, context):
    name = request.params.get('name', '')

    groups = DBSession.query(Group) \
        .filter(
            and_(
                Group.name.contains(name),
                Group.visible == True
            )
        ) \
        .order_by(Group.id) \
        .limit(5) \
        .all()

    result = {
        group.id: group.serialize(context)
        for group in groups
    }
    return result


@view_config(route_name='group.join_by_invite', renderer='json', request_method='POST')
@validate_matchdict(Param('group_invite_url', required=True))
@with_context(require_auth=True)
def group_join_by_invite(request, context):
    group_invite_url = request.matchdict['group_invite_url']
    group_invite = GroupInvite.get_by_url(group_invite_url)

    user_group = UserGroup.create_if_not_exists(
        user_id=context.user_id,
        group_id=group_invite.group_id
    )
    joined = bool(user_group)
    if joined:
        DBSession.add(user_group)

    response = {
        'joined': joined,
        'redirect': group_invite.redirect
    }

    return response
