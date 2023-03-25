import json

from pyramid.view import view_config

from sqlalchemy import desc, asc

from pynformatics.models import DBSession
from pynformatics.view.utils import GetUserIds

@view_config(route_name='group.get_enrolled', renderer='json')
def get_user_enrolled_user_get(request):
    cmid = int(request.matchdict['cmid'])
    moodle_group_id = int(request.matchdict['group_id'])

    res = GetUserIds(request, cmid, moodle_group_id)

    return res

