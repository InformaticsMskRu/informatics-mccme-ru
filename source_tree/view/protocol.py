from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc
from mako.template import Template
from json import loads
import lxml.html


from pynformatics.view.utils import RequestGetUserId
from source_tree.utils.capability import (
    check_capability, 
    check_capability_ex
)


@view_config(route_name="protocol", renderer="protocol.mak")
def protocol(request):
    try:
        run_id = request.params['run_id'] 
        contest_id, run_id_str = run_id.split('r')
        run_id = int(run_id_str)

        contest_id = "0" * (6 - len(contest_id)) + contest_id
        run_id_str = "0" * (6 - len(run_id_str)) + run_id_str

        d = [run_id_str]
        for i in range(4):
            c = run_id % 32 
            if i:
                d.append(str(c) if c < 10 else chr(ord('A') + c - 10))
            run_id //= 32
        d.reverse()

        path = "/home/judges/" + str(contest_id) + "/var/archive/xmlreports/" + "/".join(d)

        tests = []
        f = open(path)
        data = f.read(512000)
        doc = lxml.html.document_fromstring(data)
        for test in doc.cssselect("tests > test"):
            tests.append({
                "status": test.get("status"),
                "time": int(test.get("time")) / 1000,
                "real-time": int(test.get("real-time")) / 1000,
                "memory": test.get("max-memory-used"),
                "score": test.get("score"),
                "nominal-score": test.get("nominal-score"),
            })
        
        
        f.close()
        
        return {
            "tests": tests,
        }
    except Exception as e:
        return Response("Error: " + e.__str__())
