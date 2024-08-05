from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, Stars
import sys, traceback
from phpserialize import *
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload

@view_config(route_name='stars.add', request_method='GET', renderer='json')
def add(request):
    try:
        link = html.escape(request.params['link'])
        user_id = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        stars = DBSession.query(Stars).filter_by(user_id=user_id.id).filter_by(link=link).all()
        for star in stars:
            DBSession.delete(star)
        title = html.escape(request.params['title'])
        stars = Stars(user_id, title, link)
        with transaction.manager:
            DBSession.add(stars);
        return {"result" : "ok"}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='stars.delete', request_method='GET', renderer='json')
def delete(request):
    try:
        link = html.escape(request.params['link'])
        user_id = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        stars = DBSession.query(Stars).filter_by(user_id=user_id.id).filter_by(link=link).all()
        for star in stars:
            DBSession.delete(star)
        return {"result" : "ok"}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='stars.get_by_user_id_html', renderer='pynformatics:templates/stars.mak')
@view_config(route_name='stars.get_by_user_id', renderer='json')
def get_by_user_id(request):
    res = {"stars" : []}
    stars = DBSession.query(Stars).filter(Stars.user_id == RequestGetUserId(request)).order_by(Stars.id).all()
    for star in stars:
        res["stars"].append(star.__json__(request))
    return res


