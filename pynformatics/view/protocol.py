import sys, traceback
import time
import json
import transaction
import zipfile
from xml.etree.ElementTree import ElementTree
from collections import OrderedDict
from pyramid.view import view_config
from pynformatics.model import User, EjudgeContest, Run, Comment, EjudgeProblem, Problem, Statement
from pynformatics.contest.ejudge.serve_internal import EjudgeContestCfg
from pynformatics.view.utils import *
from phpserialize import *
from pynformatics.view.utils import *
from pynformatics.models import DBSession
from pynformatics.models import DBSession
from pynformatics.model.run import to32
from pynformatics.utils.check_role import *

signal_description = {
    1 : "Hangup detected on controlling terminal or death of controlling process",
    2 : "Interrupt from keyboard",
    3 : "Quit from keyboard",
    4 : "Illegal Instruction",
    6 : "Abort signal",
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
            if (run.user.statement.filter(Statement.olympiad == 1).filter(Statement.timestop > time.time()).filter(Statement.timestart < time.time()).count() == 0):
                res = OrderedDict()
                for num in range(1, len(run.tests.keys()) + 1):
                    res[str(num)] = run.tests[str(num)]
                print(run.host)
                return {"tests": res, "host": run.host}
            else:
                try:
                    return [run.tests["1"]]
                except KeyError as e:
                    return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}
        except Exception as e:
            return {"result" : "error", "message" : run.compilation_protocol, "error" : e.__str__(), "stack" : traceback.format_exc()}
    except Exception as e: 
        return {"result" : "error", "message" : e.__str__(), "stack" : traceback.format_exc()}


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

@view_config(route_name="protocol.get_full", renderer="json")
@check_global_role(("teacher", "ejudge_teacher", "admin"))
def protocol_get_full(request):
    try:
        contest_id = int(request.matchdict['contest_id'])
        run_id = int(request.matchdict['run_id'])
        run = Run.get_by(run_id = run_id, contest_id = contest_id)
        prob = run.problem
        out_path = "/home/judges/{0:06d}/var/archive/output/{1}/{2}/{3}/{4:06d}.zip".format(
            contest_id, to32(run_id // (32 ** 3) % 32), to32(run_id // (32 ** 2) % 32), to32(run_id // 32 % 32), run_id
        )
        try:
            prot = get_protocol(request)
            if "result" in prot and prot["result"] == "error":
                return prot
            
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


                if "checker" in judge_info:
                    prot[test_num]["checker_output"] = judge_info["checker"]
                if "stderr" in judge_info:
                    prot[test_num]["error_output"] = judge_info["stderr"]
                if "output" in judge_info:
                    prot[test_num]["output"] = judge_info["output"]

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
        except Exception as e:
            return {"result": "error", "content": e.__str__(), "out_path": out_path}
    except Exception as e:
        return {"result": "error", "content": e.__str__()}
