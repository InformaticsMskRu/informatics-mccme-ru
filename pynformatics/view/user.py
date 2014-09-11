from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Run, PynformaticsUser, EjudgeUser
import sys, traceback
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload
from sqlalchemy import desc
from sqlalchemy.ext.serializer import dumps, loads

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

@view_config(route_name='rating.get', renderer='json')
def get_rating(request):    
    #parse_params
    bad_params = dict()
    try:
        if  request.params['page'] != '':
            length = int(request.params['length']  
        else:
            length = 10
    except Exception e:
        length = 10
        bad_params['length'] = request.params['length']

    try:
        if page in request.params and request.params['page'] != '':
            start = int(request.params['page']) * length
        else:
            start = 0
    except Exception e:
        start = 0
        bad_params['start'] = request.params['start']

    try:
        if '-' in request.params['solved_filter']:
            solved_from_filter, solved_to_filter = map(int, request.params['solved_filter'].split('-'))
        else:
            solved_from_filter, solved_to_filter = int(request.params['solved_filter']), int(request.params['solved_filter'])
    except Exception e:
        solved_from_filter, solved_to_filter = None, None
        bad_params['solved_filter'] = request.params['solved_filter']

    try:
        if '-' in request.params['week_solved_filter']:
            week_solved_from_filter, week_solved_to_filter = map(int, request.params['week_solved_filter'].split('-'))
        else:
            week_solved_from_filter, week_solved_to_filter = int(request.params['week_solved_filter']), int(request.params['week_solved'_filter])
    except Exception e:
        week_solved_from_filter, week_solved_to_filter = None, None
        bad_params['week_solved_filter'] = request.params['week_solved_filter']

    city = request.params['city_filter']
    name = request.params['name_filter']



    user_count = DBSession.query(User).filter(User.deleted == False).count()

    if (city):
        filter_user_count = DBSession.query(User).filter(User.deleted == False).filter(EjudgeUser.city.like(city_search)).count()
        users = DBSession.query(EjudgeUser).filter(EjudgeUser.deleted == False).filter(EjudgeUser.city.like(city_search)).order_by(desc(EjudgeUser.problems_solved)).slice(start, start + length)
    else:
        filter_user_count = user_count
        users = DBSession.query(EjudgeUser).filter(EjudgeUser.deleted == False).order_by(desc(EjudgeUser.problems_solved)).slice(start, start + length)
    res = []
    for user in users:
        week_query = DBSession.execute("SELECT COUNT(DISTINCT contest_id, prob_id) FROM ejudge.runs as r WHERE r.user_id=:uid AND r.create_time > (NOW() - INTERVAL 7 DAY) AND (r.status=0 OR r.status=8)", 
           {"uid" : user.ejudge_id} )
        week_count = week_query.scalar()
        res.append({'name':user.firstname + " " + user.lastname, 'solved':user.problems_solved, 'place': None, 'city':user.city, 'solved_week' : week_count})

    #place generation
    res.sort(key=lambda el: -el['solved'])
    for ind in range(len(res)):
        res[ind]['place'] = ind + 1 + start
    
    return {
            "data" : res,
            "recordsTotal" : user_count,
            "recordsFiltered" : filter_user_count,
            "dump" : str(request.params)
            "bad_params" : bad_params
            }

