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

@view_config(route_name='rating.get', renderer='json')
def get_rating(request):    
    #parse_params
    bad_params = dict()
    try:
        if  request.params['length'] != '':
            length = int(request.params['length'])
        else:
            length = 10
    except Exception as e:
        length = 10
        bad_params['length'] = request.params.get('length', None)

    try:
        if 'page' in request.params and request.params['page'] != '':
            start = (int(request.params['page']) - 1) * length
        else:
            start = 0
    except Exception as e:
        start = 0
        bad_params['page'] = request.params.get('page', None)

    try:
        if '-' in request.params['solved_filter']:
            solved_from_filter, solved_to_filter = map(int, request.params['solved_filter'].split('-'))
        else:
            solved_from_filter, solved_to_filter = int(request.params['solved_filter']), int(request.params['solved_filter'])
    except Exception as e:
        solved_from_filter, solved_to_filter = None, None
        bad_params['solved_filter'] = request.params.get('solved_filter', None)

    try:
        if '-' in request.params['week_solved_filter']:
            week_solved_from_filter, week_solved_to_filter = map(int, request.params['week_solved_filter'].split('-'))
        else:
            week_solved_from_filter, week_solved_to_filter = int(request.params['week_solved_filter']), int(request.params['week_solved_filter'])
    except Exception as e:
        week_solved_from_filter, week_solved_to_filter = None, None
        bad_params['week_solved_filter'] = request.params.get('week_solved_filter', None)

    city = request.params.get('city_filter', None)
    name = request.params.get('name_filter', None)



    user_count = DBSession.query(User).filter(User.deleted == False).count()
    #current_selection = DBSession.query(User).filter(User.deleted == False)

    # if city is not None:
    #     current_selection = current_selection.filter(EjudgeUser.city.like('%' + city + '%'))
    # if name is not None:
    #     current_selection = current_selection.filter(or_(EjudgeUser.firstname.like('%' + name + '%'), EjudgeUser.lastname.like('%' + name + '%')))
    # if None not in (solved_from_filter, solved_to_filter):
    #     current_selection = current_selection.filter(solved_from_filer <= EjudgeUser.problems_solved <= solved_to_filter)
    # current_selection = current_selection.order_by(desc(EjudgeUser.problems_solved)).slice(start, start + length)
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
        #if None not in (week_solved_from_filter, week_solved_to_filter) and week_solved_from_filter <= week_count <= week_solved_to_filter:
        res.append({'name':user.firstname + " " + user.lastname, 'solved':user.problems_solved, 'place': None, 'city':user.city, 'solved_week' : week_count})

    #place generation
    # first, last, current_place = 0, 0, 1
    # while first < len(res):
    #     while res[last]['solved'] == res[first]['solved'] and last < len(res):
    #         last += 1
    #         res[last]['place'] = current_place
    #     current_place += 1
    #     first = last

    return {
            "data" : res,
            "recordsTotal" : user_count,
            "recordsFiltered" : filter_user_count,
            "dump" : str(request.params),
            "bad_params" : bad_params
            }

