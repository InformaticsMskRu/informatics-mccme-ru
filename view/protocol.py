from pyramid.view import view_config
from pynformatics.model import User, EjudgeUser, EjudgeContest, Run, Comment, EjudgeProblem, Problem, Statement
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.view.utils import *
import sys, traceback
#import jsonpickle, demjson
import time
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
import transaction
#import jsonpickle, demjson
import json
from pynformatics.models import DBSession
#from webhelpers.html import *
from xml.etree.ElementTree import ElementTree
from collections import OrderedDict

@view_config(route_name='protocol.get', renderer='json')
def get_protocol(request):
    try:
        contest_id = int(request.matchdict['contest_id'])
        run_id = int(request.matchdict['run_id'])
        run = Run.get_by(run_id = run_id, contest_id = contest_id)
#        checkCapability(request)
        try:
            run.tested_protocol
#            if 1 == 1:
#                return "1"
            if (True or run.user.statement.filter(Statement.olympiad == 1).filter(Statement.timestop > time.time()).filter(Statement.timestart < time.time()).count() == 0):
                res = OrderedDict()
                for num in range(1, len(run.tests.keys()) + 1):
                    res[str(num)] = run.tests[str(num)]
#                    if res[str(num)]['status'] != "OK": 
#                        break
                return res
            else:
                try:
#                    st = run.user.statement.filter(Statement.olympiad == 1).filter(Statement.timestop > time.time()).first()
#                    return str(time.time()) + " " + str(st.id)
                    return [run.tests["1"]]
                except Exception as e:
                    return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}
        except Exception as e:
#            return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}        
            return {"message" : run.compilation_protocol, "error" : e.__str__(), "stack" : traceback.format_exc()}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}
