from pyramid.view import view_config
from pynformatics.model import User, EjudgeContest, EjudgeRun, Comment, EjudgeProblem, Problem, Statement
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.view.utils import *
import sys, traceback
#import jsonpickle, demjson
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
import transaction
#import jsonpickle, demjson
import json
from pynformatics.models import DBSession
#from webhelpers.html import *
from xml.etree.ElementTree import ElementTree

@view_config(route_name='team_monitor.get', renderer='string')
def get_team_monitor(request):
    try:
        statement_id = int(request.matchdict['statement_id'])
    
        user = DBSession.query(User).filter(User.id == RequestGetUserId(request)).first()
        statement = DBSession.query(Statement).filter(Statement.id == statement_id).first()
#        checkCapability(request)
        res = ""
        for k, v in statement.problems.items():
            res = res + "[" + str(k) + "] " + v.name
        return statement.name + " " + res
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}
