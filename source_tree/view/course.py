from pyramid.response import Response
from pyramid.view import view_config
import json

from source_tree.models import (
    db_session, 
    Course, 
)

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.course import *



@view_config(route_name='course.get_by_author', renderer='json')
def course_get_by_author(request):
    try:
        author_id = int(request.matchdict['author_id'])
        if author_id != int(RequestGetUserId(request)):
            return {'result': 'error', 'content': 'Access denied'}
        courses = course_get_by_user(author_id)
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

