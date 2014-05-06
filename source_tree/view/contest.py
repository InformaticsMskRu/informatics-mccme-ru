from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from mako.template import Template
from json import loads

from source_tree.models import db_session, Source, Problem, StatementProblem

from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import (
    check_capability, 
    check_capability_ex
)
from source_tree.utils.session import (
    get_php_session_object, 
    update_php_session_object
)
from source_tree.utils.source import source_add_by_dict


@view_config(route_name='contest.add.source', renderer='json')
def contest_add_source(request):
    try:
        check_capability(request, 'admin')
        statement_id = request.matchdict['contest_id']
        source_id = request.matchdict['source_id']
        statement_problems = db_session.query(StatementProblem).filter(
                StatementProblem.statement_id == statement_id).order_by(StatementProblem.rank).all()
        for i in range(len(statement_problems)):
            letter = ''
            cur = i + 1
            while cur:
                cur -= 1
                letter = chr(ord('A') + cur % 26) + letter
                cur //= 26

            source_add_by_dict({
                'name': 'Задача ' + letter,
                'parent_id': source_id,
                'order': (i + 1) * 10**7,
                'author': RequestGetUserId(request),
                'verified': True,
                'problem_id': statement_problems[i].problem_id
            })
        db_session.commit()
        return {"result": "ok"}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}


@view_config(route_name='contest.set.source', renderer='contest_set_source.mak')
def contest_set_source(request):
    return {'contest_id': request.matchdict['contest_id']}
