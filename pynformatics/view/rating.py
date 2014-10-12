from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Run, PynformaticsUser, User, Group, UserGroup
import sys, traceback
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload
from sqlalchemy import desc, asc
from sqlalchemy.ext.serializer import dumps, loads
import sqltap


def generate_places(users_data_list, current_selection, filter_user_count, start):
    first, last, start_place = start, start, current_selection.filter(User.problems_solved > users_data_list[0]['solved']).count() + 1
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
                    users_data_list[i]['place'] = str(start_place)
            start_place = last + 1
    last_place = filter_user_count - current_selection.filter(User.problems_solved < users_data_list[-1]['solved']).count()
    for i in range(first - start, last - start):
        if start_place != last_place:
            users_data_list[i]['place'] = "{0}-{1}".format(start_place, last_place)
        else:
            users_data_list[i]['place'] = str(start_place)
    return users_data_list

def generate_current_user_data(current_selection, filter_user_count, current_user_id, res):
    user_data = None
    if current_user_id != -1 and current_selection.filter(User.id == current_user_id).count():
        user, group = current_selection.filter(User.id == current_user_id).first()
        start_place = current_selection.filter(User.problems_solved > user.problems_solved).count() + 1
        last_place = filter_user_count - current_selection.filter(User.problems_solved < user.problems_solved).count()
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
    #star sqltap
    profiler = sqltap.start()

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
    group_list = request.params.get('group_list', None)

    group_filter = request.params.get('group_filter', None)
    try:
        if group_filter == '':
            group_filter = None
        else:
            group_filter = int(group_filter)
    except Exception as e:
        bad_params['group_filter'] = group_filter

    #quering from database
    cuser_id = int(RequestGetUserId(request))
    user_count = DBSession.query(User).filter(User.deleted == False).count()

    current_selection = DBSession.query(User, UserGroup).filter(UserGroup.group_id  == group_filter).filter(UserGroup.user_id == User.id)
    if city is not None:
        current_selection = current_selection.filter(User.city.like('%' + city + '%'))
    if school is not None:
        current_selection = current_selection.filter(User.school.like('%' + school + '%'))

    if None not in (solved_from_filter, solved_to_filter):
        current_selection = current_selection.filter(User.problems_solved.between(solved_from_filter, solved_to_filter))

    if name is not None:
        current_selection = current_selection.filter(User.lastname.like('%' + name + '%'))
    filter_user_count = current_selection.count()
    current_selection = current_selection.order_by(desc(User.problems_solved))
    page_selection = current_selection.slice(start, start + length) 

    query = str(page_selection)

    if group_list is not None:
        group_list = [{'name' : group.name, 'id' : group.id} for group, ug in DBSession.query(Group, UserGroup).filter(UserGroup.user_id == cuser_id).filter(Group.id == UserGroup.group_id).order_by(asc(Group.name)).all()]

    #forming result data
    res = []
    if filter_user_count > 0:

        for user, user_group in page_selection:
            week_query = DBSession.execute("SELECT COUNT(DISTINCT contest_id, prob_id) FROM ejudge.runs as r WHERE r.user_id=:uid AND r.create_time > (NOW() - INTERVAL 7 DAY) AND (r.status=0 OR r.status=8)", 
            {"uid" : user.ejudge_id} )
            week_count = week_query.scalar()
            firstname, lastname = "", ""
            if user.firstname != None:
                firstname = user.firstname
            if user.lastname != None:
                lastname = user.lastname
            res.append({'name':firstname + " " + lastname, 'solved':user.problems_solved, 'school':user.school, 'place': None, 'city':user.city, 'solved_week':week_count})
        generate_places(res, current_selection, filter_user_count, start)
    cuser_data = generate_current_user_data(current_selection, filter_user_count, cuser_id, res)

    #sqltap statistic report
    statistics = profiler.collect()
    sqltap.report(statistics, "report.html")
    

    return {
            "data" : res,
            "recordsTotal" : user_count,
            "recordsFiltered" : filter_user_count,
            "dump" : str(request.params),
            "bad_params" : bad_params,
            "current_user_data" : cuser_data,
            "group_list" : group_list,
            "query" : query
            }

