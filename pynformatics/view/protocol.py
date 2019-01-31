import traceback
import zipfile
from io import BytesIO

import requests
from pynformatics import EjudgeProblem
from pyramid.response import Response
from pyramid.view import view_config
from pynformatics.models import DBSession

from pynformatics.model import Run
from pynformatics.model.run import get_lang_ext_by_id
from pynformatics.utils.check_role import check_global_role
from pynformatics.utils.request_helpers import require_captcha

signal_description = {
    1: "Hangup detected on controlling terminal or death of controlling process",
    2: "Interrupt from keyboard",
    3: "Quit from keyboard",
    4: "Illegal Instruction",
    6: "Abort signal",
    7: "Bus error (bad memory access)",
    8: "Floating point exception",
    9: "Kill signal",
    11: "Invalid memory reference",
    13: "Broken pipe: write to pipe with no readers",
    14: "Timer signal",
    15: "Termination signal"
}

PROTOCOL_EXCLUDED_FIELDS = ['audit']
PROTOCOL_EXCLUDED_TEST_FIELDS = [
    'input', 'big_input', 'corr',
    'big_corr', 'output', 'big_output',
    'checker_output', 'error_output', 'extra'
]


@view_config(route_name='protocol.get', renderer='json')
def get_protocol(request):
    # Короче в чём разница protocol и full protocol
    # В full_protocol есть audit
    # И в тестах (protocol[tests] возвращает iterable)
    # А в protocol[tests][i] лежат дополнительно:
    # [input, big_input, corr, big_corr, output,
    #  big_output, checker_output, error_output, extra]
    run_id = int(request.matchdict['run_id'])
    url = 'http://localhost:12346/problem/run/{}/protocol'.format(run_id)
    response = requests.get(url)
    content = response.json()

    if content['status'] != 'success':
        return content

    data = content['data']
    for field in PROTOCOL_EXCLUDED_FIELDS:
        data.pop(field, None)
    tests = data.get('tests')

    if not tests:
        return data

    for test in tests.values():
        for field in PROTOCOL_EXCLUDED_TEST_FIELDS:
            test.pop(field, None)

    return data


@view_config(route_name="protocol.get_full", renderer="json")
@check_global_role(("ejudge_teacher", "admin"))
def protocol_get_full(request):
    # Короче в чём разница protocol и full protocol
    # В full_protocol есть audit
    # И в тестах (protocol[tests] возвращает iterable)
    # А в protocol[tests][i] лежат дополнительно:
    # [input, big_input, corr, big_corr, output,
    #  big_output, checker_output, error_output, extra]
    run_id = int(request.matchdict['run_id'])

    url = 'http://localhost:12346/problem/run/{}/protocol'.format(run_id)
    response = requests.get(url)
    content = response.json()

    if content['status'] != 'success':
        return content

    return content['data']


@view_config(route_name="protocol.get_test", renderer="string")
@check_global_role(("ejudge_teacher", "admin"))
def protocol_get_test(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id=run_id, contest_id=contest_id)
    prob = run.problem
    return prob.get_test(int(request.matchdict['test_num']),
                         prob.get_test_size(int(request.matchdict['test_num'])))


@view_config(route_name="protocol.get_corr", renderer="string")
@check_global_role(("ejudge_teacher", "admin"))
def protocol_get_corr(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id=run_id, contest_id=contest_id)
    prob = run.problem
    return prob.get_corr(int(request.matchdict['test_num']),
                         prob.get_corr_size(int(request.matchdict['test_num'])))


@view_config(route_name="protocol.get_outp", renderer="string")
@check_global_role(("ejudge_teacher", "admin"))
def protocol_get_outp(request):
    contest_id = int(request.matchdict['contest_id'])
    run_id = int(request.matchdict['run_id'])
    run = Run.get_by(run_id=run_id, contest_id=contest_id)
    return run.get_output_file(int(request.matchdict['test_num']), tp='o')


@require_captcha
@view_config(route_name="protocol.get_submit_archive", renderer="string")
@check_global_role(("ejudge_teacher", "admin"))
def get_submit_archive(request):

    request_source = "sources" in request.params
    run_id = int(request.matchdict['run_id'])
    problem_id = int(request.params['problem_id'])
    request_all_tests = "all_tests" in request.params

    if not request_all_tests:
        require_test_numbers = request.params.get("tests", "")
        if require_test_numbers:
            tests_numbers_set = set(map(int, require_test_numbers.split(' ')))
        else:
            tests_numbers_set = set()
    else:
        # TODO: Здесть не 100, а некое максимальное число тестов
        # TODO: Его можно было найти в EjudgeRun.tests_count,
        # TODO: который брался из протокола
        # TODO: Но мы это пофиксили
        tests_numbers_set = list(range(1, 100))

    archive = BytesIO()
    zip_file = zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED)

    if request_source:
        # Download source and info about run
        url = 'http://localhost:12346/problem/run/{}/source/'.format(run_id)
        try:
            resp = requests.get(url, {'is_admin': True})
            resp.raise_for_status()
        except (requests.RequestException, ValueError) as e:
            print('Request to :12346 failed!')
            print(str(e))
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

        content = resp.json()
        data = content['data']
        lang_id = data['language_id']
        request_source = data['source']

        # Write source
        source_name = "{0}{1}".format(run_id, get_lang_ext_by_id(lang_id))
        zip_file.writestr(source_name, request_source)

    # TODO: Перенести логику выкачивания тестов проблем в rmatics/ejudge-core
    ejudge_problem = DBSession.query(EjudgeProblem).get(problem_id)

    # Write tests
    for num in tests_numbers_set:
        try:
            test_data = ejudge_problem.get_test(num, ejudge_problem.get_test_size(num))
            answer_data = ejudge_problem.get_corr(num, ejudge_problem.get_corr_size(num))

            zip_file.writestr("tests/{0:02}".format(num), test_data)
            zip_file.writestr("tests/{0:02}.a".format(num), answer_data)
        except FileNotFoundError:
            break

    # Write checkers
    checker_src, checker_ext = ejudge_problem.get_checker()
    zip_file.writestr("checker{}".format(checker_ext), checker_src)

    zip_file.close()
    archive.seek(0)

    response = Response(content_type="application/zip",
                        content_disposition='attachment; filename="archive_{0}_{1}.zip"'.format(
                            problem_id, run_id),
                        body=archive.read())
    return response

