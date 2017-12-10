import traceback

from pyramid.view import view_config

from pynformatics.model.group import Group
from pynformatics.model.group import UserGroup
from pynformatics.models import DBSession
from pynformatics.utils.context import with_context


@view_config(route_name='group.get', renderer='json')
@with_context
def get_group(request, context):
    try:
        group_id = int(request.matchdict['group_id'])
        group = DBSession.query(Group).filter(Group.id == group_id).first()
        if group is None:
            return {
                "result": "error",
                "message": "group with id = {} not found".format(group_id)
            }

        group = group.serialize()
        users = DBSession.query(UserGroup).filter(UserGroup.group_id == group_id).all()
        for i in range(len(users)):
            users[i] = users[i].user.serialize(context)

        return {
            "group": group,
            "users": users
        }

    except Exception as e:
        return {
            "result": "error",
            "message": e.__str__(),
            "stack": traceback.format_exc()
        }
