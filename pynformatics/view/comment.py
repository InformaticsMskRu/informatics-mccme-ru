from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Run, Comment, EjudgeProblem
import sys, traceback
from phpserialize import *
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html

from sqlalchemy import or_
from sqlalchemy.orm import noload, lazyload

@view_config(route_name='comment.add', request_method='POST', renderer='json')
def add(request):
    try:
        if (not RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')):
            raise Exception("Auth Error")

        author_id = RequestGetUserId(request)

        run_id = request.params['run_id']
        user_id = request.params['user_id']

        # Это XSS
        lines = html.escape(request.params['lines'])
        comment = html.escape(request.params['comment'])

        date = datetime.datetime.now()

        commentary = Comment(run_id=run_id,
                             user_id=user_id,
                             author_user_id=author_id,
                             date=date,
                             lines=lines,
                             comment=comment,
                             is_read=False)

        with transaction.manager:
            DBSession.add(commentary)
        return {"result": "ok"}
    except Exception as e: 
        return {"result": "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

class CommentRes:
    pass     


@view_config(route_name='comment.get_all_html', renderer='pynformatics:templates/comment.get_table.mak')   
@view_config(route_name='comment.get_all', renderer='json')
def get_all(request):
    return DBSession.query(Comment).options(noload('*')).filter(Comment.user_id == RequestGetUserId(request)).order_by(Comment.is_read).order_by(Comment.date.desc()).all()
    

@view_config(route_name='comment.get_all_limit_html', renderer='pynformatics:templates/comment.get_table.mak')   
@view_config(route_name='comment.get_all_limit', renderer='json')
def get_all_limit(request):
    start = int(request.matchdict['start'])
    stop = int(request.matchdict['stop'])
    res = {"comment" : []}
    q = DBSession.query(Comment).filter(Comment.user_id == RequestGetUserId(request)).order_by(Comment.is_read).order_by(Comment.date.desc()).slice(start, stop)
    comments = q.all()
    for c in comments:
        res["comment"].append(c.__json__(request))
    res["query"] = str(q)
    res["user_id"] = RequestGetUserId(request)
    return res


@view_config(route_name='comment.get_unread_limit_html', renderer='pynformatics:templates/comment.get_table.mak')   
@view_config(route_name='comment.get_unread_limit', renderer='json')
def get_unread_limit(request):
    start = int(request.matchdict['start'])
    stop = int(request.matchdict['stop'])
    res = {"comment" : []}
    q = DBSession.query(Comment).filter(Comment.user_id == RequestGetUserId(request)).filter(Comment.is_read == False).order_by(Comment.date.desc()).slice(start, stop)
    comments = q.all()
    for c in comments:
        res["comment"].append(c.__json__(request))
    res["query"] = str(q)
    res["user_id"] = RequestGetUserId(request)
    return res

    
@view_config(route_name='comment.get_count', renderer='json')
def get_count(request):
    return DBSession.query(Comment).filter(Comment.user_id == RequestGetUserId(request)).count()


class JSONDateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
           return obj.isoformat()
        else:
           return super(DateTimeJSONEncoder, self).default(obj)


@view_config(route_name='comment.get_count_unread', renderer='json')
def get_count_unread(request):
    jsonpickle.set_preferred_backend('demjson')
    jsonpickle.set_encoder_options('json', cls=JSONDateTimeEncoder)
    res = DBSession.query(Comment).filter(Comment.user_id == RequestGetUserId(request)).filter(Comment.is_read == False).count()
    return jsonpickle.encode(res, unpicklable = False, max_depth = 5)


@view_config(route_name='comment.get', renderer='string')
def get(request):
    try:
        run_id = int(request.matchdict['run_id'])
        is_superuser = RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')
        user_id = RequestGetUserId(request)

        comment_q = DBSession.query(Comment).filter(Comment.py_run_id == run_id)
        if not is_superuser:
            comment_q.filter(or_(Comment.author_user_id == user_id,
                                 Comment.user_id == user_id))
        comments = comment_q.all()

        jsonpickle.set_preferred_backend('demjson')
        jsonpickle.set_encoder_options('json', cls=JSONDateTimeEncoder)

        return jsonpickle.encode(comments, unpicklable=False, max_depth=5)

    except Exception as e:
        return json.dumps({"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()})
