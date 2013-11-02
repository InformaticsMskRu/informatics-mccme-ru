from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, EjudgeUser, Run, PynformaticsUser
import sys, traceback
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload

@view_config(route_name='user_settings.add', request_method='POST', renderer='json')
def add(request):
    try:
        if (not RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')):
            raise Exception("Auth Error")
        run = Run.get_by(run_id = request.params['run_id'], contest_id = request.params['contest_id'])
        if not run:
            raise Exception("Object not found")
        user = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        comment = Comment(run, user, html.escape(request.params['lines']), html.escape(request.params['comment']));
        with transaction.manager:
            DBSession.add(comment);
        return {"result" : "ok"}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='user_settings.get', renderer='string')
def get(request):
    try:
        user_id = request.matchdict['user_id']
        if ( int(user_id) != int(RequestGetUserId(request))):            
            raise Exception("Auth Error")
    except Exception as e: 
        return json.dumps({"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()})



