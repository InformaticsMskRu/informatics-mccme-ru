import sys, traceback
import time
import json
import transaction
import zipfile
from io import BytesIO
from xml.etree.ElementTree import ElementTree
from collections import OrderedDict

from pyramid.view import view_config
from pyramid.response import Response

from pynformatics.model import User, EjudgeContest, Run, Comment, EjudgeProblem, Problem, Statement
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.view.utils import *
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
from pynformatics.models import DBSession
from pynformatics.model.run import to32, get_lang_ext_by_id
from pynformatics.utils.check_role import check_global_role


# signal_description = {
#     1 : "Hangup detected on controlling terminal or death of controlling process",
#     2 : "Interrupt from keyboard",
#     3 : "Quit from keyboard",
#     4 : "Illegal Instruction",
#     6 : "Abort signal",
#     7 : "Bus error (bad memory access)",
#     8 : "Floating point exception",
#     9 : "Kill signal",
#     11 : "Invalid memory reference",
#     13 : "Broken pipe: write to pipe with no readers",
#     14 : "Timer signal",
#     15 : "Termination signal"
# }


@view_config(route_name='protocol.get', renderer='json')
def get_protocol(request):
    try:
        contest_id = int(request.matchdict['contest_id'])
        run_id = int(request.matchdict['run_id'])
        run = Run.get_by(run_id=run_id, contest_id=contest_id)
        try:
            run.fetch_tested_protocol_data()
            if run.user.statement.filter(
                        Statement.olympiad == 1
                    ).filter(
                Statement.time_stop > time.time()
                    ).filter(
                Statement.time_start < time.time()
                    ).count() == 0:
                res = OrderedDict()
                if run.tests:
                    sample_tests = run.problem.sample_tests.split(',')
                    for num in range(1, len(run.tests.keys()) + 1):
                        str_num = str(num)
                        if str_num in sample_tests:
                            res[str_num] = run.get_test_full_protocol(str_num)
                        else:
                            res[str_num] = run.tests[str_num]
                return {
                    'tests': res,
                    'host': run.host,
                    'compiler_output': run.compiler_output,
                }
            else:
                try:
                    return {
                        'tests': run.tests['1'],
                        'host': run.host,
                        'compiler_output': run.compiler_output,
                    }
                except KeyError as e:
                    return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}
        except Exception as e:
            return {"result" : "error", "message" : run.compilation_protocol, "error" : e.__str__(), "stack" : traceback.format_exc(), "protocol": run.protocol}
    except Exception as e:
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc(), "protocol": run.protocol}


@view_config(route_name="protocol.get_full", renderer="json")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def protocol_get_full(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id=run_id, contest_id=contest_id)
    protocol = get_protocol(request)
    if protocol.get('result') == "error":
        return protocol

    prot = protocol.get('tests', {})
    out_arch = None

    for test_num in prot:
        prot[test_num] = run.get_test_full_protocol(test_num)

    if out_arch:
        out_arch.close()

    full_protocol = {
        'tests': prot,
        'audit': run.get_audit(),
    }
    if protocol.get('compiler_output'):
        full_protocol['compiler_output'] = protocol['compiler_output']
    return full_protocol


@view_config(route_name="protocol.get_test", renderer="string")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def protocol_get_test(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id = run_id, contest_id = contest_id)
    prob = run.problem
    return prob.get_test(int(request.matchdict['test_num']), prob.get_test_size(int(request.matchdict['test_num'])))


@view_config(route_name="protocol.get_corr", renderer="string")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def protocol_get_corr(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id = run_id, contest_id = contest_id)
    prob = run.problem
    return prob.get_corr(int(request.matchdict['test_num']), prob.get_corr_size(int(request.matchdict['test_num'])))


@view_config(route_name="protocol.get_outp", renderer="string")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def protocol_get_outp(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id = run_id, contest_id = contest_id)
    return run.get_output_file(int(request.matchdict['test_num']), tp='o')


@view_config(route_name="protocol.get_submit_archive", renderer="string")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def get_submit_archive(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    sources = "sources" in request.params
    all_tests = "all_tests" in request.params
    tests = request.params.get("tests", "")
    tests_set = set()
    for i in tests.split(" "):
        try:
            tests_set.add(int(i))
        except ValueError:
            pass

    run = Run.get_by(run_id = run_id, contest_id = contest_id)
    run.parsetests
    prob = run.problem
    archive = BytesIO()
    zf = zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED)

    run.fetch_tested_protocol_data()
    for i in range(1, run.tests_count + 1):
        if all_tests or i in tests_set:
            zf.writestr("tests/{0:02}".format(i), prob.get_test(i, prob.get_test_size(i)))
            zf.writestr("tests/{0:02}.a".format(i), prob.get_corr(i, prob.get_corr_size(i)))

    if sources:
        zf.writestr("{0}{1}".format(run_id, get_lang_ext_by_id(run.lang_id)), run.get_sources())

    checker_src, checker_ext = prob.get_checker()
    zf.writestr("checker{}".format(checker_ext), checker_src)

    zf.close()
    archive.seek(0)
    response = Response(content_type="application/zip", content_disposition='attachment; filename="archive_{0}_{1}.zip"'.format(contest_id, run_id), body=archive.read())
    return response
