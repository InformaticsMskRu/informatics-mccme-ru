from pyramid.view import view_config

from pynformatics.model.group import Group
from pynformatics.model.group import UserGroup
from pynformatics.model.user import User
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import GroupNotFound


@view_config(route_name='group.get', renderer='json')
@with_context
def get_group(request, context):
    group_id = int(request.matchdict['group_id'])
    group = DBSession.query(Group).filter(Group.id == group_id).first()
    if group is None:
        raise GroupNotFound()

    owner = DBSession.query(User).filter(User.id == group.owner_id).first().serialize(context)
    users = DBSession.query(UserGroup).filter(UserGroup.group_id == group_id).all()
    for i in range(len(users)):
        users[i] = users[i].user.serialize(context)

    group = group.serialize()
    del group['owner_id']
    group.update({
        'owner': owner,
        'users': users
    })
    return group
