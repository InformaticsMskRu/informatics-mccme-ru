from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc
from mako.template import Template
from json import loads

from source_tree.models import db_session, Source, Problem, StatementProblem

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import (
    check_capability, 
    check_capability_ex
)
from source_tree.utils.problem import problem_get_by_id
from source_tree.utils.source import *


@view_config(route_name='source.add', renderer='json')
def source_add(request):
    try:
        check_capability(request, 'admin')
        add_dict = dict(request.params)
        names = request.params['name'].split('\n')
        order, order_right = map(int, request.params['order'].split(':'))
        order_shift = (order_right - order) / (len(names) + 1)
        for name in names:
            order += order_shift
            add_dict['name'] = name
            add_dict['order'] = order
            add_dict['verified'] = True
            add_dict['author'] = RequestGetUserId(request)
            source_add_by_dict(add_dict)
        db_session.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.update', renderer='json')
def source_update(request):
    try:
        check_capability(request, 'admin')
        source = source_get_by_id(request.matchdict['source_id'])
        for field in request.params:
            if field in ['name', 'parent_id', 'order', 'problem_id', 'verified']:
                source.__setattr__(field, request.params[field])
        source.author = RequestGetUserId(request)
        db_session.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.erase', renderer='json')
def source_erase(request):
    try:
        check_capability(request, 'edit')
        source = source_get_by_id(request.matchdict['source_id'])
        if source.get_type() != '_subject' or not source.problem_id:
            check_capability(request, 'admin')
        db_session.delete(source)
        db_session.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.erase.all', renderer='json')
def source_erase_all(request):
    def erase_tree(source):
        if not source:
            return
        for child in source.children:
            erase_tree(child)
        db_session.delete(source)
    try:
        check_capability(request, 'admin')
        source = source_get_by_id(request.matchdict['source_id'])
        erase_tree(source)
        db_session.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.verify', renderer='json')
def source_verify(request):
    try:
        check_capability(request, 'edit')
        source = source_get_by_id(request.matchdict['source_id'])
        source.verified = True
        db_session.commit()
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='source.verify.cancel', renderer='json')
def source_verify_cancel(request):
    try:
        check_capability(request, 'edit')
        source = source_get_by_id(request.matchdict['source_id'])
        if source.verified:
            raise Exception("Source mustn't be canceled")
        db_session.delete(source)
        db_session.commit()
        return {'result': 'ok'}
    except Exception as e:
        return {'result': 'error', 'content': e.__str__()}


@view_config(route_name='source.get.children', renderer='json')
def source_get_children(request):
    source = source_get_by_id(request.matchdict['source_id'])
    return {
        'children': [child for child in source.children if not child.problem_id]
            + [child for child in source.children if child.problem_id]
    }


@view_config(route_name='source.get', renderer='json')
def source_get(request):
    source = source_get_by_id(request.matchdict['source_id'])
    return source


@view_config(route_name='source.get.all', renderer='json')
def source_get_all(request):
    source_type = '_' + request.matchdict['source_type']
    root = db_session.query(Source).filter(
        Source.parent_id == 1, 
        Source.name == source_type
    ).one()
    return source_get_all_by_node(root)


@view_config(route_name='source.get.all.to_verify', renderer='json')
def source_get_all_to_verify(request):
    source_type = '_' + request.matchdict['source_type']
    sources = db_session.query(Source).filter(Source.verified == False).order_by(Source.time).all()    
    sources = [{
        'source': source,
        'parent': source.parent,
        'problem': {
            'id': source.problem.id,
            'name': source.problem.name
        },
        'user': {
            'id': source.user.id,
            'firstname': source.user.firstname,
            'lastname': source.user.lastname
        }
    } for source in sources if source.get_type() == source_type]
    return sources


@view_config(route_name='source.dir', renderer='source_dir.mak')
def source_dir(request):
    try:
        query_id = request.matchdict['source_id'].split('-')
        cur_page, page_size = [int(request.params[field]) \
            if field in request.params else default \
            for field, default in [('page', 1), ('cnt', 5)] \
        ]
        if cur_page < 0 or page_size <= 0 or page_size > 100 or len(query_id) > 2:
            raise Exception("Bad params")
        source, subject = source_get_root('source'), source_get_root('subject')
        for id in query_id:
            source_new = source_get_by_id(id)
            if source_new.id == 1:
                raise Exception("Bad params")
            if source_new.parent_id == 1:
                continue
            if source_new.get_type() == '_subject':
                subject = source_new
            elif source_new.get_type() == '_source':
                source = source_new        
        sources_cnt = {}
        set_source, set_subject = set(), set()
        for cur_source, cur_set_source in [(source, set_source), (subject, set_subject)]:
            for child in cur_source.children:
                if child.problem_id and child.verified:
                    cur_set_source.add(child.problem_id)
                else:
                    child_problems = source_get_problems_all(child)
                    sources_cnt[child] = len(child_problems)
                    cur_set_source |= child_problems
        problems_id_set = set_source & set_subject \
            if not source.is_root() and not subject.is_root() \
            else set_source if not source.is_root() \
            else set_subject
        problems = db_session.query(Problem).filter(Problem.id.in_(set(problems_id_set)))\
            .order_by(Problem.id)[(cur_page - 1)*page_size : cur_page*page_size]
        problems_cnt = len(problems_id_set)
        problems_subjects = {}
        problems_sources = {}
        for dict_sources, source_type in [(problems_subjects, '_subject'), \
                (problems_sources, '_source')]:
            for problem in problems:
                dict_sources[problem] = [subject for subject in \
                    db_session.query(Source).filter(Source.problem_id == problem.id, Source.verified == 1).all() \
                    if subject.get_type() == source_type
                ]
        page_cnt = (problems_cnt + page_size - 1) // page_size
        center_page = min(max(cur_page - 1, 3), max(page_cnt - 4, 0))
        page_list = range(max(center_page - 3, 0), min(center_page + 4, page_cnt)) if page_cnt else [0]
        return {
                'source': source,
                'source_path': source.get_path()[1:],
                'source_children': source_get_children_without_problems(source),
                'subject': subject,
                'subject_path': subject.get_path()[1:],
                'subject_children': source_get_children_without_problems(subject),
                'sources_cnt': sources_cnt,
                'problems': problems,
                'problems_cnt': problems_cnt,
                'problems_subjects': problems_subjects,
                'problems_sources': problems_sources,
                'cur_page': cur_page,
                'page_size': page_size,
                'page_list': page_list,
                'contest_add': request.session['basket'] if 'basket' in request.session else None
        }
    except Exception as e:
        return Response("Error: " + e.__str__())


@view_config(route_name='source.dir.home')
def source_dir_home(request):
    subject_root = db_session.query(Source).filter(
        Source.parent_id == 1, 
        Source.name == '_subject'
    ).one()
    return exc.HTTPFound(request.route_url('source.dir', source_id=subject_root.id))

@view_config(route_name='source.dir.contest.current', renderer='json')
def source_dir_contest_current(request):
    try:
        basket = request.session['basket']
        return {
            "result": "ok", 
            "contest_id": basket.contest_id,
            "course_id": basket.course_id
        }
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.dir.contest.add_problem', renderer='json')
def source_dir_contest_add_problem(request):
    try:
        problem = problem_get_by_id(request.matchdict['problem_id'])
        request.session['basket'].add(problem.id)
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.dir.contest.erase_problem', renderer='json')
def source_dir_contest_erase_problem(request):
    try:
        ind = int(request.matchdict['problem_index'])
        request.session['basket'].erase(ind)
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}
        

@view_config(route_name='source.dir.contest.move_problem', renderer='json')
def source_dir_contest_move_problem(request):
    try:
        ind = int(request.matchdict['problem_index'])
        move_type = request.matchdict['move_type']
        request.session['basket'].move(ind, move_type)
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.dir.contest.get_problems', renderer='json')
def source_dir_contest_get_problems(request):
    try:
        basket = request.session['basket']
        problems = [db_session.query(Problem).filter(Problem.id == id).one() 
            for id in basket.problems]
        return {
            "result": "ok", 
            "problems": [{
                "id": problem.id,
                "name": problem.name
            } for problem in problems]    
        }
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.dir.contest.clean', renderer='json')
def source_dir_contest_clean(request):
    try:
        del request.session['manage_contest']
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='source.dir.contest.new')
def source_dir_contest_new(request):
    try:
        check_capability(request, 'manage_contest')
        contest_id, course_id = map(int, request.matchdict['contest'].split('-'))
        request.session['basket'] = Basket(contest_id, course_id)
        return exc.HTTPFound(request.route_url('source.dir.home'))
    except Exception as e:
        return exc.HTTPForbidden() if e.__str__() == 'Access denied'else exc.HTTPInternalServerError()


@view_config(route_name='source.dir.contest.create')
def source_dir_contest_create(request):
    try:
        check_capability(request, 'manage_contest')
        basket = request.session['basket']
        for i in range(len(basket.problems)):
            db_session.add(StatementProblem(
                basket.contest_id, 
                basket.problems[i], 
                i + 1
        ))
        db_session.commit()
        course_id = basket.course_id
        del request.session['basket']
        return exc.HTTPFound(location='/moodle/mod/statements/view.php?id=' + str(course_id))
    except Exception as e:
        return exc.HTTPForbidden() if e.__str__() == 'Access denied' else exc.HTTPInternalServerError()


@view_config(route_name='source.adm', renderer='source_adm.mak')
def source_adm(request):
    return {}


@view_config(route_name='source.adm.form', renderer='source_adm_form.mak')
def source_adm_frame(request):
    return {}


@view_config(route_name='subject.adm', renderer='subject_adm.mak')
def subject_adm(request):
    return {}
