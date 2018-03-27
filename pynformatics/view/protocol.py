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



signal_description = {
    1 : "Hangup detected on controlling terminal or death of controlling process",
    2 : "Interrupt from keyboard",
    3 : "Quit from keyboard",
    4 : "Illegal Instruction",
    6 : "Abort signal",
    7 : "Bus error (bad memory access)",
    8 : "Floating point exception",
    9 : "Kill signal",
    11 : "Invalid memory reference",
    13 : "Broken pipe: write to pipe with no readers",
    14 : "Timer signal",
    15 : "Termination signal"
}

@view_config(route_name='protocol.get', renderer='json')
def get_protocol(request):
    try:
        contest_id = int(request.matchdict['contest_id'])
        run_id = int(request.matchdict['run_id'])
        run = Run.get_by(run_id = run_id, contest_id = contest_id)
        try:
            run.tested_protocol
            ret = {
                'host': run.host,
                'display_checker_comments': run.display_checker_comments,
            }
            if (run.user.statement.filter(Statement.olympiad == 1).filter(Statement.timestop > time.time()).filter(Statement.timestart < time.time()).count() == 0):
                res = OrderedDict()
                for num in range(1, len(run.tests.keys()) + 1):
                    res[str(num)] = run.tests[str(num)]
                ret["tests"] = res
                return ret
            else:
                try:
                    ret["tests"] = run.tests["1"]
                    return ret
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
    run = Run.get_by(run_id = run_id, contest_id = contest_id)
    prob = run.problem
    out_path = "/home/judges/{0:06d}/var/archive/output/{1}/{2}/{3}/{4:06d}.zip".format(
        contest_id, to32(run_id // (32 ** 3) % 32), to32(run_id // (32 ** 2) % 32), to32(run_id // 32 % 32), run_id
    )
    prot = get_protocol(request)
    if "result" in prot and prot["result"] == "error":
        return prot

    prot = prot["tests"]
    out_arch = None

    for test_num in prot:
        judge_info = run.judge_tests_info[test_num]

        if prob.get_test_size(int(test_num)) <= 255:
            prot[test_num]["input"] = prob.get_test(int(test_num))
            prot[test_num]["big_input"] = False
        else:
            prot[test_num]["input"] = prob.get_test(int(test_num)) + "...\n"
            prot[test_num]["big_input"] = True

        if prob.get_corr_size(int(test_num)) <= 255:
            prot[test_num]["corr"] = prob.get_corr(int(test_num))
            prot[test_num]["big_corr"] = False
        else:
            prot[test_num]["corr"] = prob.get_corr(int(test_num)) + "...\n"
            prot[test_num]["big_corr"] = True

        try:
            if run.get_output_file_size(int(test_num), tp='o') <= 255:
                prot[test_num]["output"] = run.get_output_file(int(test_num), tp='o')
                prot[test_num]["big_output"] = False
            else:
                prot[test_num]["output"] = run.get_output_file(int(test_num), tp='o', size=255) + "...\n"
                prot[test_num]["big_output"] = True
        except OSError as e:
            prot[test_num]["output"] = judge_info.get("output", "")
            prot[test_num]["big_output"] = False


        try:
            if run.get_output_file_size(int(test_num), tp='c') <= 255:
                prot[test_num]["checker_output"] = run.get_output_file(int(test_num), tp='c')
            else:
                prot[test_num]["checker_output"] = run.get_output_file(int(test_num), tp='c', size=255) + "...\n"
        except OSError as e:
            prot[test_num]["checker_output"] = judge_info.get("checker", "")

        try:
            if run.get_output_file_size(int(test_num), tp='e') <= 255:
                prot[test_num]["error_output"] = run.get_output_file(int(test_num), tp='e')
            else:
                prot[test_num]["error_output"] = run.get_output_file(int(test_num), tp='e', size=255) + "...\n"
        except OSError as e:
            prot[test_num]["error_output"] = judge_info.get("stderr", "")

        if "term-signal" in judge_info:
            prot[test_num]["extra"] = "Signal {0}. ".format(judge_info["term-signal"]) + signal_description[judge_info["term-signal"]]
        if "exit-code" in judge_info:
            if "extra" not in prot[test_num]:
                prot[test_num]["extra"] = str()
            prot[test_num]["extra"] = prot[test_num]["extra"] + "\n Exit code {0}. ".format(judge_info["exit-code"])


        for type_ in [("o", "output"), ("c", "checker_output"), ("e", "error_output")]:
            file_name = "{0:06d}.{1}".format(int(test_num), type_[0])
            if out_arch is None:
                try:
                    out_arch = zipfile.ZipFile(out_path, "r")
                    names = set(out_arch.namelist())
                except:
                    names = {}
            if file_name not in names or type_[1] in prot[test_num]:
                continue
            with out_arch.open(file_name, 'r') as f:
                prot[test_num][type_[1]] = f.read(1024).decode("utf-8") + "...\n"

    if out_arch:
        out_arch.close()
    return {"tests": prot, "audit": run.get_audit()}

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

    run.tested_protocol
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
