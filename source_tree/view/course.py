from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc
from sqlalchemy import not_
from mako.template import Template
from json import loads
import json

from source_tree.models import (
    db_session, 
    Course, 
    CourseRaw,
    CourseTreeCap,
)

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import (
    check_capability_course, 
    check_capability_ex_course,
    RequestGetUserId,
)
from source_tree.utils.course import *


def course_make_dump(request):
    class Req:
        def __init__(self, request, params, matchdict):
            self.registry = request.registry
            self.params = params
            self.matchdict = matchdict
    for i in [0, 1]:
        params = {
            'show_hidden': i,
            'dump': 1,
        }
        matchdict = {
            'course_id': 1,
        }
        course_dump(Req(request, params, matchdict))


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
        course_make_dump(request)
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.erase', renderer='json')
def course_erase(request):
    return course_erase_all(request)
    try:
        raise Exception("DEPRECATED")
        course = course_get_by_id(request.matchdict['course_id'])
        if course_check_owner(course.course_id, int(RequestGetUserId(request))) \
            or course_tree_check_owner(course.id, RequestGetUserId(request)):
            check_capability_course(request, 'teacher')
        else:
            check_capability_course(request, 'admin')
        db_session.delete(course)
        db_session.commit()
        course_make_dump(request)
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


def erase_tree(course):
    for child in course.children:
        erase_tree(child)
    db_session.delete(course)


@view_config(route_name='course.erase.all', renderer='json')
def course_erase_all(request):
    try:
        course = course_get_by_id(request.matchdict['course_id'])
        teacher = False
        teacher = teacher or (not course.verified \
                              and course.author == int(RequestGetUserId(request)))
        teacher = teacher or course_check_owner(course.course_id, 
                                                int(RequestGetUserId(request)))
        teacher = teacher or course_tree_check_owner(course.id, 
                                                     RequestGetUserId(request))
        check_capability_course(request, 'teacher' if teacher else 'admin')
        erase_tree(course)
        db_session.commit()
        course_make_dump(request)
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.verify', renderer='json')
def course_verify(request):
    try:
        check_capability_course(request, 'admin')
        full_access = int(request.params.get('full_access', 0))
        course = course_get_by_id(request.matchdict['course_id'])
        course.verified = True
        if full_access:
            db_session.add(CourseTreeCap(
                node_id=course.id,
                user_id=course.author,
            ))
        db_session.commit()
        course_make_dump(request)
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='course.verify.cancel', renderer='json')
def course_verify_cancel(request):
    try:
        check_capability_course(request, 'admin')
        course = course_get_by_id(request.matchdict['course_id'])
        if course.verified:
            raise Exception("Source mustn't be canceled")
        db_session.delete(course)
        db_session.commit()
        course_make_dump(request)
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}

        
@view_config(route_name='course.get.all.to_verify', renderer='json')
def course_get_all_to_verify(request):
    categories = int(request.params.get('categories', 0))
    nodes_filter = db_session.query(Course).filter(Course.verified == False)
    if categories:
        nodes_filter = nodes_filter.filter(Course.course_id == 0)
    else:
        nodes_filter = nodes_filter.filter(Course.course_id > 0)
    nodes = nodes_filter.order_by(Course.time).all()    
    result = []
    for node in nodes:
        res_item = {
            'node': node,
            'parent': node.parent,
        }
        if node.course:
            res_item.update({
                'course': {
                    'id': node.course.id,
                    'name': node.course.fullname
                },
            })
        if node.user:
            res_item.update({
                'user': {
                    'id': node.user.id,
                    'firstname': node.user.firstname,
                    'lastname': node.user.lastname
                }
            })

        result.append(res_item)
    return result


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
        course_make_dump(request)
        return {"result": "ok", "content": {
            "new_id": ids,
        }}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='course.adm', renderer='course/adm.mak')
def course_adm(request):
    try:   
        course_id = request.params['course_id'] if 'course_id' in request.params else None
        course = db_session.query(CourseRaw).filter(CourseRaw.id == course_id).one() \
            if course_id else None
        return {
            'course': course,
        }
    except Exception as e:
        return Response("Error: " + e.__str__())

def get_children_by_map(childrenMap, id):
    if not id in childrenMap:
        return []
    return childrenMap[id]

@view_config(route_name='course.dump', renderer='course_dump.mak')
def course_dump(request):
    try:
        def course_update_count(course, course_count, show_hidden, childrenMap):
            course_count[course] = 1 if course.course and (show_hidden or course.course.visible) else 0
            children = get_children_by_map(childrenMap, course.id)
            for child in children:
                if not show_hidden and not child.visible:
                    continue
                course_count[course] += course_update_count(child, course_count, show_hidden, childrenMap)
            return course_count[course]

        dump = request.params['dump'] if 'dump' in request.params else 0
        show_hidden = request.params['show_hidden'] if 'show_hidden' in request.params else 0
        course_root = db_session.query(Course).filter(Course.id == request.matchdict['course_id']).one()
        displayed_courses = db_session.query(Course).filter(Course.displayed == 1).all()
        course_count = {}
        courses = db_session.query(Course).order_by(
            Course.parent_id,
            Course.order,
        ).all()
        childrenMap = {}
        for course in courses:
            if not course.parent_id in childrenMap:
                childrenMap[course.parent_id] = []
            childrenMap[course.parent_id].append(course)
        course_update_count(course_root, course_count, show_hidden, childrenMap)
        default_storage = json.dumps({
            "#region{0}".format(course_root.id): int(course_root.displayed) \
                for course_root in displayed_courses 
        })
        
        if dump:
            filename = "course_dump" + ("_show_hidden" if show_hidden else "") + ".php"
            filepath = request.registry.settings['source_tree.course.dump_path'] + filename
            dump_file = open(filepath, "w", encoding="utf-8")
            dump_file.write(Template(filename=request.registry.settings["source_tree.project_path"] \
                    + "/source_tree/templates/course_dump.mak", input_encoding="utf-8").render_unicode(
                course_root=course_root,
                show_hidden=show_hidden,
                dump=dump,
                course_count=course_count,
                default_storage=default_storage,
                childrenMap=childrenMap,
                get_children_by_map=get_children_by_map,
            ))
            dump_file.close()

            return Response("ok. dumped to {0}".format(filepath))
        else:
            return {
                'course_root': course_root,
                'show_hidden': show_hidden,
                'dump': dump,
                'course_count': course_count,
                'default_storage': default_storage,
                'childrenMap': childrenMap,
                'get_children_by_map': get_children_by_map,
            }
    except Exception as e:
        return Response("Error: " + e.__str__())


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


@view_config(route_name='course.my_categories', renderer='course/my_categories.mak')
def course_my_categories(request):
    try:
        frame = int(request.params.get('frame', 1))
        course_root = db_session.query(Course).filter(Course.id == 1).one() 
        course_list = []
        make_course_list(course_root, course_list, 0)
        my_nodes = db_session.query(Course).filter(
            Course.course_id == 0,
            Course.author == RequestGetUserId(request),
        ).order_by(Course.verified).all()
        my_verified_nodes = [node for node in my_nodes if node.verified]
        my_unverified_nodes = [node for node in my_nodes if not node.verified]
        root_nodes = course_tree_get_root_nodes(RequestGetUserId(request))
        '''
        my_nodes = [node for node in my_nodes if node in root_nodes] + \
                    [node for node in my_nodes if node not in root_nodes]
        '''
        return {
            'frame': frame,
            'course_list': course_list,
            'my_nodes': my_nodes,
            'my_unverified_nodes': my_unverified_nodes,
            'root_nodes': root_nodes,
            'default_storage': json.dumps({}),
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
                'has_password': course.password != '',
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


@view_config(route_name='course.all', renderer='course/all.mak')
def course_all(request):
    try:
        check_capability_course(request, 'admin')
        courses_res = []
        courses = db_session.query(CourseRaw).\
            filter(CourseRaw.category.in_([24, 34])).all()
        for course in courses:
            nodes = db_session.query(Course).filter(Course.course_id == course.id).all()
            paths = [node.parent.full_name() + ("" if node.verified else " (не разобрано)") \
                for node in nodes]
            courses_res.append({
                'course': course,
                'paths': paths,
                'authors': course_get_users(course.id),
            })  
        return {
            'courses': courses_res,
        }
    except Exception as e:
        return Response("Error: " + e.__str__())

        
@view_config(route_name='course.verify_list', renderer='course/verify_list.mak')
def course_verify_list(request):
    categories = request.params.get('categories', 0)
    return {
        'categories': categories,
    }
