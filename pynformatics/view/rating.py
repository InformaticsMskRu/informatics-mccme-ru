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
#import sqltap
from sqlalchemy import func

class RatingRequestParams:
    def __init__(self, request):
        self.bad_params = dict()

        #parse length
        try:
            if  request.params['length'] != '':
                self.length = int(request.params['length'])
            else:
                self.length = 10
        except Exception as e:
            self.length = 10
            self.bad_params['length'] = request.params.get('length', None)

        #calculate current page
        try:
            if 'page' in request.params and request.params['page'] != '':
                self.start = (int(request.params['page']) - 1) * self.length
            else:
                self.start = 0
        except Exception as e:
            self.start = 0
            self.bad_params['page'] = request.params.get('page', None)

        #parse filter by count of solved problem params
        try:
            if '-' in request.params['solved_filter']:
                self.solved_from_filter, self.solved_to_filter = map(int, request.params['solved_filter'].split('-'))
            else:
                self.solved_from_filter, self.solved_to_filter = int(request.params['solved_filter']), int(request.params['solved_filter'])
        except Exception as e:
            self.solved_from_filter, self.solved_to_filter = None, None
            self.bad_params['solved_filter'] = request.params.get('solved_filter', None)

        #parse filter by count of solved by week problem params
        try:
            if '-' in request.params['solved_week_filter']:
                self.week_solved_from_filter, self.week_solved_to_filter = sorted(list(map(int, request.params['solved_week_filter'].split('-'))))
            else:
                self.week_solved_from_filter, self.week_solved_to_filter = int(request.params['solved_week_filter']), int(request.params['solved_week_filter'])
        except Exception as e:
            self.week_solved_from_filter, self.week_solved_to_filter = None, None
            self.bad_params['solved_week_filter'] = request.params.get('solved_week_filter', None)

        #parse city, name, school filters
        self.city = request.params.get('city_filter', '')
        self.name = request.params.get('name_filter', '')
        self.school = request.params.get('school_filter', '')

        #parse group_list param (if it's not None, then we send list of group)
        self.group_list = request.params.get('group_list', None)

        #parse filter 
        self.group_filter = request.params.get('group_filter', None)
        try:
            if self.group_filter == '':
                self.group_filter = None
            else:
                self.group_filter = int(self.group_filter)
        except Exception as e:
            self.group_filter = None
            self.bad_params['group_filter'] = self.group_filter


def generate_places(users_data_list, current_selection, current_count_selection, filter_user_count, start):
    first, last, start_place = start, start, current_count_selection.filter(User.problems_solved > users_data_list[0]['solved']).scalar() + 1
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
    last_place = start_place + current_count_selection.filter(User.problems_solved == users_data_list[-1]['solved']).scalar() - 1
    for i in range(first - start, last - start):
        if start_place != last_place:
            users_data_list[i]['place'] = "{0}-{1}".format(start_place, last_place)
        else:
            users_data_list[i]['place'] = str(start_place)
    return users_data_list

def generate_current_user_data(current_selection, current_count_selection, filter_user_count, current_user_id, res):
    user_data = None
    if current_user_id != -1 and current_count_selection.filter(User.id == current_user_id).scalar():
        user = current_selection.filter(User.id == current_user_id).first()
        start_place = current_count_selection.filter(User.problems_solved > user.problems_solved).scalar() + 1
        last_place = start_place + current_count_selection.filter(User.problems_solved == user.problems_solved).scalar() - 1
        user_data = { 'id':current_user_id, 'name':user.firstname + " " + user.lastname, 'solved':user.problems_solved, 'place': None, 'school':user.school, 'city':user.city, 'solved_week':user.problems_week_solved}
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


#problems_week_solved

@view_config(route_name='rating.get', renderer='json')
def get_rating(request):
    #star sqltap
    #profiler = sqltap.start()

    #parse_params
    params = RatingRequestParams(request)

    #quering from database
    cuser_id = int(RequestGetUserId(request))
    user_count = DBSession.query(func.count(User.id)).filter(User.deleted == False).scalar()

    current_selection = DBSession.query(User).filter(User.deleted == False)
    current_count_selection = DBSession.query(func.count(User.id)).filter(User.deleted == False)

    if params.group_filter not in [None, 2]: #2 - group_id for group with all users, we don't need to filter by that
        current_selection = current_selection.filter(UserGroup.group_id  == params.group_filter).filter(UserGroup.user_id == User.id)
        current_count_selection = current_count_selection.filter(UserGroup.group_id  == params.group_filter).filter(UserGroup.user_id == User.id)

    if params.city is not None:
        current_selection = current_selection.filter(User.city.like('%' + params.city + '%'))
        current_count_selection = current_count_selection.filter(User.city.like('%' + params.city + '%'))
    
    if params.school is not None:
        current_selection = current_selection.filter(User.school.like('%' + params.school + '%'))
        current_count_selection = current_count_selection.filter(User.school.like('%' + params.school + '%'))

    if None not in (params.solved_from_filter, params.solved_to_filter):
        current_selection = current_selection.filter(User.problems_solved.between(params.solved_from_filter, params.solved_to_filter))
        current_count_selection = current_count_selection.filter(User.problems_solved.between(params.solved_from_filter, params.solved_to_filter))

    if None not in (params.week_solved_from_filter, params.week_solved_to_filter):
        current_selection = current_selection.filter(User.problems_week_solved.between(params.week_solved_from_filter, params.week_solved_to_filter))
        current_count_selection = current_count_selection.filter(User.problems_week_solved.between(params.week_solved_from_filter, params.week_solved_to_filter))


    if params.name is not None:
        current_selection = current_selection.filter(User.lastname.like('%' + params.name + '%'))
        current_count_selection = current_count_selection.filter(User.lastname.like('%' + params.name + '%'))

    filter_user_count = current_count_selection.scalar()
    current_selection = current_selection.order_by(desc(User.problems_solved))
    page_selection = current_selection.slice(params.start, params.start + params.length) 

    query = str(current_count_selection)

    group_list = None
    if params.group_list is not None:
        group_list = [{'name' : group.name, 'id' : group.id} for group, ug in DBSession.query(Group, UserGroup).filter(UserGroup.user_id == cuser_id).filter(Group.id == UserGroup.group_id).order_by(asc(Group.name)).all()]

    #forming result data
    res = []
    if filter_user_count > 0:

        for user in page_selection:
            firstname, lastname = "", ""
            if user.firstname != None:
                firstname = user.firstname
            if user.lastname != None:
                lastname = user.lastname
            res.append({'id':user.id, 'name':firstname + " " + lastname, 'solved':user.problems_solved, 'school':user.school, 'place': None, 'city':user.city, 'solved_week':user.problems_week_solved})
        generate_places(res, current_selection, current_count_selection, filter_user_count, params.start)
    cuser_data = generate_current_user_data(current_selection, current_count_selection, filter_user_count, cuser_id, res)
    #sqltap statistic report
    statistics = profiler.collect()
    #sqltap.report(statistics, "report.html")
    

    return {
            "data" : res,
            "recordsTotal" : user_count,
            "recordsFiltered" : filter_user_count,
            "dump" : str(request.params),
            "bad_params" : params.bad_params,
            "current_user_data" : cuser_data,
            "group_list" : group_list,
            "query" : query
            }

