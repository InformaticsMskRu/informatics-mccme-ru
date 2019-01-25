from pyramid.view import view_config
from pynformatics.view.utils import *
import traceback

import json



@view_config(route_name='user_settings.get', renderer='string')
def get(request):
    try:
        user_id = request.matchdict['user_id']
        if ( int(user_id) != int(RequestGetUserId(request))):
            raise Exception("Auth Error")
    except Exception as e:
        return json.dumps({"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()})
