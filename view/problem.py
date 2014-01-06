from pyramid.view import view_config
from pynformatics.model import User, EjudgeContest, Run, Comment, EjudgeProblem, Problem
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
import os
from pynformatics.models import DBSession
#from webhelpers.html import *
from xml.etree.ElementTree import ElementTree
import xmlrpc.client

def checkCapability(request):
    if (not RequestCheckUserCapability(request, 'moodle/ejudge_contests:reload')):
        raise Exception("Auth Error")

def setShowLimits(problem_id, show_limits):    
    problem = DBSession.query(Problem).filter(Problem.id == problem_id).first()

    problem.show_limits = show_limits
    with transaction.manager:
        DBSession.merge(problem) 
    return "Ok"
    
        
@view_config(route_name='problem.limits.show', renderer='string')
def problem_show_limits(request):
    try:
        checkCapability(request)
        return setShowLimits(request.matchdict['problem_id'], 1)
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

	
@view_config(route_name='problem.submit', renderer='string')
def problem_show_limits(request):
    return "result"	

@view_config(route_name='problem.tests.set_preliminary', renderer='json')
def problem_set_preliminary(request):
    try:
        checkCapability(request)
        problem = DBSession.query(Problem).filter(Problem.id == request.matchdict['problem_id']).first()

        problem.sample_tests = request.params['sample_tests']
        with transaction.manager:
           DBSession.merge(problem) 
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e: 
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.generate_samples', renderer='json')
def problem_generate_samples(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        problem.generateSamples()
#        res = ""
#        if problem.sample_tests != '':
#            res = "<div class='problem-statement'><div class='sample-tests'><div class='section-title'>Примеры</div>"
#        
#            for i in problem.sample_tests.split(","):
#                res += "<div class='sample-test'>"
#                res += "<div class='input'><div class='title'>Входные данные</div><pre class='content'>"
#                res += get_test(problem, i)
#                res += "</pre></div><div class='output'><div class='title'>Выходные данные</div><pre class='content'>"
#                res += get_corr(problem, i)
#                res += "</pre></div></div>"
#        
#            res += "</div></div>"
#
#        problem.sample_tests_html = res
        with transaction.manager:
           DBSession.merge(problem) 
        return {"result" : "ok", "content" : problem.sample_tests}
    except Exception as e: 
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.limits.hide', renderer='string')
def problem_hide_limits(request):
    try:
        checkCapability(request)
        return setShowLimits(request.matchdict['problem_id'], 0)
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

@view_config(route_name='problem.tests.count', renderer='string')
def problem_get_tests_count(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)
        cnt = 0
        res = ""
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            if os.path.exists(test_file_name):
                res += test_file_name
            else:
                break
        return cnt - 1
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}

#def get_test(problem, test_num):
#    conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
#    prob = conf.getProblem(problem.problem_id)
#
#    test_file_name = (prob.tests_dir + prob.test_pat) % int(test_num)
#    if os.path.exists(test_file_name):
#        f = open(test_file_name)
#        res = f.read(255)
#    else:
#        res = test_file_name
#    return res

#def get_corr(problem, test_num):
#    conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
#    prob = conf.getProblem(problem.problem_id)
#
#    corr_file_name = (prob.tests_dir + prob.corr_pat) % int(test_num)
#    if os.path.exists(corr_file_name):
#        f = open(corr_file_name)
#        res = f.read(255)
#    else:
#        res = corr_file_name
#    return res


@view_config(route_name='problem.tests.get_test', renderer='json')
def problem_get_test(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()

        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_test(test_num)}
    except Exception as e: 
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.add', renderer='json')
def problem_add_test(request):
    try:
        checkCapability(request)
        s = xmlrpc.client.ServerProxy('http://localhost:7080/')

        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
        conf = EjudgeContestCfg(number = problem.ejudge_contest_id)
        prob = conf.getProblem(problem.problem_id)

        cnt = 0
        flag = False
        while True:
            cnt += 1
            test_file_name = (prob.tests_dir + prob.test_pat) % cnt
            corr_file_name = (prob.tests_dir + prob.corr_pat) % cnt
            if not os.path.exists(test_file_name):
                flag = True
                break

        if flag:
            s.add_file(test_file_name, request.params['input_data'])
            s.add_file(corr_file_name, request.params['output_data'])
        return {"result" : "ok", "content" : test_file_name}        
    except Exception as e: 
        return {"result" : "error", "content" : e.__str__(), "stack" : traceback.format_exc()}


@view_config(route_name='problem.tests.get_corr', renderer='json')
def problem_get_corr(request):
    try:
        checkCapability(request)
        problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == request.matchdict['problem_id']).first()
    
        test_num = request.matchdict['test_num']
        return {"num" : int(test_num), "content" : problem.get_corr(test_num)}
    except Exception as e: 
        return {"result" : "error", "num" : int(request.matchdict['test_num']), "content" : e.__str__(), "stack" : traceback.format_exc()}