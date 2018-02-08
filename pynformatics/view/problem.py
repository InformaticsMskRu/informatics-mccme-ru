import io
import logging
import os
import traceback
import transaction
import xmlrpc.client
from pyramid.view import view_config

from pynformatics.contest.ejudge.ejudge_proxy import submit
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.model.user import SimpleUser
from pynformatics.model.problem import (
    EjudgeProblem,
    Problem,
)
from pynformatics.model.pynformatics_run import PynformaticsRun
from pynformatics.models import DBSession
from pynformatics.view.utils import *
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import (
    EjudgeError,
    Forbidden,
)
from pynformatics.utils.validators import (
    validate_matchdict,
    validate_params,
    IntParam,
    Param,
)


LOG = logging.getLogger(__name__)


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


@view_config(route_name='problem.submit', renderer='json')
@with_context(require_auth=True)
def problem_submits(request, context):
    lang_id = request.params['lang_id']
    input_file = request.POST['file'].file
    filename = request.POST['file'].filename
    ejudge_url = request.registry.settings['ejudge.new_client_url']
    return {
        'res': submit(
            run_file=input_file,
            contest_id=context.problem.ejudge_contest_id,
            prob_id=context.problem.problem_id,
            lang_id=lang_id,
            login=context.user.login,
            password=context.user.password,
            filename=filename,
            url=ejudge_url,
            user_id=context.user_id,
        )
    }


@view_config(route_name='problem.submit_v2', renderer='json', request_method='POST')
@validate_params(
    IntParam('lang_id', required=True),
    Param('file', required=True),
    IntParam('statement_id'),
)
@with_context(require_auth=True)
def problem_submits_v2(request, context):
    lang_id = int(request.params['lang_id'])
    file = request.params['file']
    filename = request.params['file'].filename
    ejudge_url = request.registry.settings['ejudge.new_client_url']

    if lang_id not in context.get_allowed_languages():
        raise Forbidden('Language id "%s" is not allowed' % lang_id)

    ejudge_response = submit(
        run_file=file.file,
        contest_id=context.problem.ejudge_contest_id,
        prob_id=context.problem.problem_id,
        lang_id=lang_id,
        login=context.user.login,
        password=context.user.password,
        filename=filename,
        url=ejudge_url,
        user_id=context.user_id,
    )
    if ejudge_response['code'] != 0:
        raise EjudgeError(ejudge_response['message'])

    run_id = ejudge_response['run_id']
    run = PynformaticsRun(
        run_id=run_id,
        contest_id=context.problem.ejudge_contest_id,
        statement_id=getattr(context.statement, 'id', None),
        source=file.value,
    )
    DBSession.add(run)

    return {}


@view_config(route_name='problem.ant.submit', renderer='json')
def problem_ant_submits(request):
    user_id = RequestGetUserId(request)
    user = DBSession.query(SimpleUser).filter(SimpleUser.id == user_id).first()
    lang_id = 67
    run_id1 = request.params["run_id1"]
    run_id2 = request.params["run_id2"]
    run_id3 = request.params["run_id3"]
    run_id4 = request.params["run_id4"]
    map_index = 0
    try:
        map_index = request.params["map_index"]
    except:
        pass
    json_names = request.params["json_names"]
    problem_id = request.matchdict["problem_id"]
    problem = DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == problem_id).first()
    #input_file = request.POST['file'].file
    #filename = request.POST['file'].filename
    filename = "input_file.txt"
    input_file = io.StringIO("{4}${5}\n{0}\n{1}\n{2}\n{3}".format(run_id1, run_id2, run_id3, run_id4, json_names, map_index))
    ejudge_url = request.registry.settings['ejudge.new_client_url']
    return {'res' : submit(input_file, problem.ejudge_contest_id, problem.problem_id, lang_id, user.login, user.password, filename, ejudge_url, user_id)}
    

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


@view_config(route_name='problem.get', renderer='json')
@with_context
def problem_get(request, context):
    return context.problem.serialize(context)


@view_config(route_name='problem.runs', renderer='json')
@validate_matchdict(IntParam('problem_id', required=True))
@with_context(require_auth=True)
def problem_runs(request, context):
    runs = context.problem.runs.filter_by(user_id=int(context.user.ejudge_id))
    runs_dict = {
        run.run_id: run.serialize()
        for run in runs
    }
    return runs_dict
