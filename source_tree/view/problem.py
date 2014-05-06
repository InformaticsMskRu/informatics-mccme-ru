from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from mako.template import Template

from source_tree.models import db_session, Source, Problem

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import check_capability, check_capability_ex
from source_tree.utils.source import source_add_by_dict, source_get_by_id
from source_tree.utils.problem import *


@view_config(route_name='problem.add.source', renderer='json')
def problem_add_source(request):
    try:
        check_capability(request, 'user')
        problem_id = request.matchdict['problem_id']
        subject_id = request.matchdict['subject_id']
        problem = problem_get_by_id(problem_id)
        subject = source_get_by_id(subject_id)
        if subject.get_type() != '_subject':
            check_capability(request, 'admin')
        cur_subject = db_session.query(Source).filter(Source.parent_id == subject_id, Source.problem_id == problem_id).all()
        if cur_subject:
            raise Exception('Already exists')
        verified = check_capability_ex(request, 'edit')
        add_dict = {
            'name': problem.name,
            'parent_id': subject_id,
            'order': 0,
            'problem_id': problem_id,
            'author': RequestGetUserId(request),
            'verified': verified
        }
        source_add_by_dict(add_dict)
        db_session.commit()
        return {'result': 'ok', 'verified': verified}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='problem.get.source', renderer='json')
def problem_get_source(request):
    problem_id = request.matchdict['problem_id']
    source_type = '_' + request.matchdict['source_type']
    subjects_problem = db_session.query(Source).filter(Source.problem_id == problem_id).all()
    subjects_problem = [{
        'parent': source.parent,
        'source': source,
        'path': ', '.join(source.get_source_path()[2:])
    } for source in subjects_problem if source.get_type() == source_type and source.verified]
    return subjects_problem


@view_config(route_name='problem.get.source.to_verify', renderer='json')
def problem_get_source_to_verify(request):
    problem_id = request.matchdict['problem_id']
    source_type = '_' + request.matchdict['source_type']
    subjects_problem = db_session.query(Source).filter(Source.problem_id == problem_id).all()
    subjects_problem = [{
        'parent': source.parent,
        'source': source
    } for source in subjects_problem if source.get_type() == source_type and not source.verified]
    return subjects_problem


@view_config(route_name='problem.get.source.html', renderer='get_name_html.mak')
def problem_get_source_html(request):
    problem_id = request.matchdict['problem_id']
    source_type = request.matchdict['source_type']
    sources = db_session.query(Source).filter(Source.problem_id == problem_id, Source.verified).all()
    source_list = []
    for source in sources:
        if source.get_type() == '_' + source_type:
            source_list.append(source.get_path())
    return {
        'source_list': source_list,
        'source_type': source_type
    }


@view_config(route_name='problem.set.source', renderer='problem_set_source.mak')
def problem_set_source(request):
    return {
        'problem': problem_get_by_id(request.matchdict['problem_id']),
        'source_type': request.matchdict['source_type'],
        'select_cnt': 8
    }
