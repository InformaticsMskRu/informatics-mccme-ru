from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy import not_
import json

from source_tree.models import (
    db_session, 
    Course, 
    CourseRaw,
)

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import (
    check_capability_course, 
    check_capability_ex_course,
    RequestGetUserId,
)
from source_tree.utils.course import *


@view_config(route_name='course.get', renderer='json')
def course_get(request):
    try:
        course = course_get_by_id(request.matchdict['course_id'])
        return {'result': 'ok', 'course': course}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.get.children', renderer='json')
def course_get_children(request):
    try:
        course = course_get_by_id(request.matchdict['course_id'])
        return {
            'result': 'ok', 
            'children': [child for child in course.children]
        }
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.update', renderer='json')
def course_update(request):
    try:
        course = course_get_by_id(request.matchdict['course_id'])
        if course_check_owner(course.course_id, int(RequestGetUserId(request))) \
            or course_tree_check_owner(course.id, RequestGetUserId(request)):
            check_capability_course(request, 'teacher')
        else:
            check_capability_course(request, 'admin')
        for field in ['parent_id', 'name', 'order', 'verified', 'course_id', 'displayed']:
            if field in request.params:
                course.__setattr__(field, request.params[field])
        course.author = RequestGetUserId(request)
        db_session.commit()
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.add', renderer='json')
def course_add(request):
    try:
        add_dict = dict(request.params)
        names = request.params['name'].split('\n')
        order = request.params['order']
        parent_id = int(request.params['parent_id'])
        user_id = int(RequestGetUserId(request))
        if order == 'end':
            parent = db_session.query(Course).filter(
                Course.id == request.params['parent_id']
            ).one()
            max_order = max(course.order for course in parent.children) \
                if list(parent.children) else 0
            order = "{0}:{1}".format(max_order, max_order + 10**7)
        order, order_right = map(int, order.split(':'))
        order_shift = (order_right - order) / (len(names) + 1)
        ids = []
        for name in names:
            vals = name.split("+++")
            title, course_id = name, 0
            if len(vals) == 2:
                title, course_id = vals
            similar = db_session.query(Course).filter(
                Course.parent_id == request.params['parent_id'],
                Course.course_id == course_id,
            ).all()
            verified = check_capability_ex_course(request, 'admin') \
                    or bool(course_tree_check_owner(parent_id, user_id))
            if course_id:
                if similar:
                    continue
                if course_check_owner(int(course_id), int(RequestGetUserId(request))):
                    check_capability_course(request, 'teacher')
                else:
                    check_capability_course(request, 'admin')
            else:
                check_capability_course(request, 'teacher')
            
            order += order_shift
            add_dict['name'] = title
            add_dict['order'] = order
            add_dict['verified'] = verified
            add_dict['course_id'] = course_id
            add_dict['author'] = max(0, user_id)
            node_id = course_add_by_dict(add_dict)
            ids.append(node_id)
        db_session.commit()
        return {"result": "ok", "content": {
            "new_id": ids,
        }}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


def get_children_by_map(childrenMap, id):
    if not id in childrenMap:
        return []
    return childrenMap[id]


@view_config(route_name='course.add.window', renderer='course/add_course_window.mak')
def course_add_window(request):
    try:
        def course_update_count(course, course_count):
            course_count[course] = 1 if course.course and course.course.visible else 0
            for child in course.children:
                if not child.visible:
                    continue
                course_count[course] += course_update_count(child, course_count)
            return course_count[course]

        frame = int(request.params['frame']) if 'frame' in request.params else 0

        course_raw = db_session.query(CourseRaw).filter(
            CourseRaw.id == request.matchdict['course_id']
        ).one()
                
        course = db_session.query(Course).filter(Course.id == 1).one()
        course_count = {}
        course_update_count(course, course_count)

        return {
            'course': course,
            'course_raw': course_raw,
            'course_count': course_count,
            'frame': frame,
        }
    except Exception as e:
        return Response("Error: " + e.__str__())


def make_course_list(course, res, shft=0):
    if course.course_id:
        return
    if course.id != 1:
        res.append((shft, course))
    for child in course.children:
        if child.verified:
            make_course_list(child, res, shft + 1)


@view_config(route_name='course.get_for_select', renderer='course/get_for_select.mak')
def course_get_for_select(request):
    try:
        course_root = db_session.query(Course).filter(Course.id == 1).one() 
        course_list = []
        make_course_list(course_root, course_list, 0)
        return {
            'course_list': course_list,
        }
    except Exception as e:
        return Response("Error: " + e.__str__())


@view_config(route_name='course.get_not_in_list', renderer='course/get_not_in_list.mak')
def course_get_not_in_list(request):
    try:
        course_nodes = db_session.query(Course).all() 
        used_courses = [course_node.course_id for course_node in course_nodes \
            if course_node.course_id]
        courses = db_session.query(CourseRaw).filter(
            CourseRaw.category.in_([24, 34]),
            not_(CourseRaw.id.in_(used_courses)),
        ).all()
        return {
            'courses': courses,
        }
    except Exception as e:
        return Response("Error: " + str(e))

        
@view_config(route_name='course.get.nodes', renderer='json')
def course_get_nodes(request):
    try:
        nodes = db_session.query(Course).\
            filter(Course.course_id == request.matchdict['course_id']).all()
        return {
            'result': 'ok',
            'nodes': nodes,
        }
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.get_by_author', renderer='json')
def course_get_by_author(request):
    try:
        courses = course_get_by_user(request.matchdict['author_id'])
        result = []
        for course in courses:
            nodes = db_session.query(Course).filter(Course.course_id == course.id).all()
            paths = [node.parent.full_name() + ("" if node.verified \
                else " (не разобрано)") for node in nodes]
            result.append({
                'id': course.id,
                'name': course.fullname,
                'paths': paths,
                'visible': course.visible,
                # 'has_password': course.password != '',
            })
        return {
            'result': 'ok',
            'courses': result,
        }
    except Exception as e:
        return {
            'result': 'error',
            'content': e.__str__(),
        }

