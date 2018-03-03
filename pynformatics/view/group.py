from pyramid.view import view_config
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

from pynformatics.model import Group, GroupInviteLink
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import Forbidden, BadRequest
from pynformatics.utils.validators import validate_matchdict, IntParam, validate_json, EnumParam

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


@view_config(route_name='group.get_owned_by', renderer='json', request_method='GET')
@validate_matchdict(IntParam('owner_id', required=True))
def group_get_owned_by(request, *, owner_id):
    groups = DBSession.query(Group).filter(Group.owner_id == owner_id).all()
    return {'data': [group.serialize() for group in groups]}


@view_config(route_name='group.get_invite_links', renderer='json', request_method='GET')
@with_context(require_auth=True, require_roles=('admin',))
@validate_matchdict(IntParam('id', required=True))
def group_get_invite_links(request, context, *, id):
    user_id = context.user.id
    group = DBSession.query(Group).get(id)
    if group.owner_id != user_id:
        raise Forbidden("You are not an owner of group {}".format(id))
    links = DBSession.query(GroupInviteLink)\
        .filter(GroupInviteLink.group_id == id).all()
    return {'data': [elem.serialize() for elem in links]}


@view_config(route_name='group.add_invite_link', renderer='json', request_method='POST')
@with_context(require_auth=True, require_roles=('admin',))
@validate_matchdict(IntParam('id', required=True))
@validate_json(
    EnumParam(
        'redirect_type',
        values=GroupInviteLink.REDIRECT_TYPES,
        required=True
    ),
    IntParam(
        'redirect_id',
        required=True)
)
def group_add_invite_link(request, context, *, id, redirect_type, redirect_id):
    user_id = context.user.id
    group = DBSession.query(Group).get(id)
    if group.owner_id != user_id:
        raise Forbidden("You are not an owner of group {}".format(id))
    invite = GroupInviteLink(id, redirect_type, redirect_id)
    try:
        invite.get_redirect(DBSession)
    except NoResultFound:
        raise BadRequest("Can't find {} with id {}".format(redirect_type, redirect_id))
    DBSession.add(invite)
    DBSession.flush()
    return invite.serialize()


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
