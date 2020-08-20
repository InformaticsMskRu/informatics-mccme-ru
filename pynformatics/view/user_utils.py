from pyramid.view import view_config
from pynformatics.view.utils import *
from pynformatics.model import User, PynformaticsUser
import sys, traceback
import transaction
import jsonpickle, demjson
import json
import datetime
from pynformatics.models import DBSession
import html
from sqlalchemy.orm import noload, lazyload
from sqlalchemy import desc
from sqlalchemy.ext.serializer import dumps, loads

@view_config(route_name='user.query', request_method='GET', renderer='string')
def query_user(request):
    try:
        if (not RequestCheckUserCapability(request, 'moodle/ejudge_submits:comment')):
            raise Exception("Auth Error")

        with open("/var/file.txt", "r", encoding = 'utf-8') as f:
            fio = f.readlines()

        all_res = "<html><head> <meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\" /></head><body>"

        for people in fio:
            people = people.strip().split(" ")
            users = DBSession.query(User).filter(User.lastname.like("%"+people[0]+"%")).all()
            res = str(people)
            for user in users:
                res += "<a href='http://informatics.msk.ru/user/view.php?id=" + str(user.id) +  "'>" + user.firstname + " " + user.lastname + "</a>&nbsp;"
            all_res += res + "<hr/>"
        all_res += "</body></html>"
        return all_res
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


