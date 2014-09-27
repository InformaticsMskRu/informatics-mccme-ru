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


def generate_places(users_data_list, current_selection, filter_user_count, start):
    first, last, start_place = start, start, current_selection.filter(EjudgeUser.problems_solved > users_data_list[0]['solved']).count() + 1
    while last - start < len(users_data_list):
        first = last
        last += 1
        while last - start < len(users_data_list) and users_data_list[last - start]['solved'] == users_data_list[first - start]['solved']:
            last += 1
        if last - start < len(users_data_list):
            for i in range(first - start, last - start):
                if last != start_place:
                    users_data_list[i]['place'] = "{0}-{1}".format(start_place, last)
                else:
                    users_data_list[i]['place'] = start_place
            start_place = last + 1
    last_place = filter_user_count - current_selection.filter(EjudgeUser.problems_solved < users_data_list[-1]['solved']).count()
    for i in range(first - start, last - start):
        if start_place != last_place:
            users_data_list[i]['place'] = "{0}-{1}".format(start_place, last_place)
        else:
            users_data_list[i]['place'] = str(start_place)
    return users_data_list

def generate_current_user_data(current_selection, filter_user_count, current_user_id, res):
    user_data = None
    if current_user_id != -1 and current_selection.filter(EjudgeUser.id == current_user_id).count():
        user = current_selection.filter(EjudgeUser.id == current_user_id).first()
        start_place = current_selection.filter(EjudgeUser.problems_solved > user.problems_solved).count() + 1
        last_place = filter_user_count - current_selection.filter(EjudgeUser.problems_solved < user.problems_solved).count()
        week_query = DBSession.execute("SELECT COUNT(DISTINCT contest_id, prob_id) FROM ejudge.runs as r WHERE r.user_id=:uid AND r.create_time > (NOW() - INTERVAL 7 DAY) AND (r.status=0 OR r.status=8)", 
        {"uid" : user.ejudge_id} )
        week_count = week_query.scalar()
        user_data = {'name':user.firstname + " " + user.lastname, 'solved':user.problems_solved, 'place': None, 'school':user.school, 'city':user.city, 'solved_week':week_count}
        if start_place != last_place:
            user_data['place'] = "{0}-{1}".format(start_place, last_place)
        else:
            user_data['place'] = str(start_place)
        if user_data not in res:
            if user_data['solved'] >= res[0]['solved']:
                user_data['position'] = "first"
            if user_data['solved']  < res[-1]['solved']:
                user_data['position'] = "last"
    return user_data

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
            week_solved_from_filter, week_solved_to_filter = sorted(list(map(int, request.params['week_solved_filter'].split('-'))))
        else:
            week_solved_from_filter, week_solved_to_filter = int(request.params['week_solved_filter']), int(request.params['week_solved_filter'])
    except Exception as e:
        week_solved_from_filter, week_solved_to_filter = None, None
        bad_params['week_solved_filter'] = request.params.get('week_solved_filter', None)

    city = request.params.get('city_filter', None)
    name = request.params.get('name_filter', None)
    school = request.params.get('school_filter', None)


    user_count = DBSession.query(EjudgeUser).filter(EjudgeUser.deleted == False).count()
    current_selection = DBSession.query(EjudgeUser).filter(EjudgeUser.deleted == False)

    if city is not None:
        current_selection = current_selection.filter(EjudgeUser.city.like('%' + city + '%'))

    if school is not None:
        current_selection = current_selection.filter(EjudgeUser.school.like('%' + school + '%'))

    if None not in (solved_from_filter, solved_to_filter):
        current_selection = current_selection.filter(EjudgeUser.problems_solved.between(solved_from_filter, solved_to_filter))

    if name is not None:
        current_selection = current_selection.filter(EjudgeUser.lastname.like('%' + name + '%'))

    filter_user_count = current_selection.count()
    current_selection = current_selection.order_by(desc(EjudgeUser.problems_solved))
    page_selection = current_selection.slice(start, start + length) 

    res = []
    if filter_user_count > 0:
        for user in page_selection:
            week_query = DBSession.execute("SELECT COUNT(DISTINCT contest_id, prob_id) FROM ejudge.runs as r WHERE r.user_id=:uid AND r.create_time > (NOW() - INTERVAL 7 DAY) AND (r.status=0 OR r.status=8)", 
            {"uid" : user.ejudge_id} )
            week_count = week_query.scalar()
            res.append({'name':user.firstname + " " + user.lastname, 'solved':user.problems_solved, 'school':user.school, 'place': None, 'city':user.city, 'solved_week':week_count})

        generate_places(res, current_selection, filter_user_count, start)
        cuser_data = generate_current_user_data(current_selection, filter_user_count, int(RequestGetUserId(request)), res)

    return {
            "data" : res,
            "recordsTotal" : user_count,
            "recordsFiltered" : filter_user_count,
            "dump" : str(request.params),
            "bad_params" : bad_params,
            "current_user_data" : cuser_data
            }

