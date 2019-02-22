import random
import string

import requests
import transaction
from pyramid.encode import urlencode
from pyramid.view import view_config, view_defaults
from pynformatics.model import User
import traceback

from pynformatics.model.monitor import MonitorLink
from pynformatics.view.monitor.monitor_renderer import MonitorRenderer
from pynformatics.view.utils import *
from pynformatics.models import DBSession


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


@view_defaults(route_name='monitor')
class MonitorApi:
    def __init__(self, request):
        self.request = request
        self.view_name = 'Monitor'

    @view_config(route_name='monitor_create', request_method='POST', renderer='json')
    def create(self):
        if not RequestCheckUserCapability(self.request, 'moodle/ejudge_submits:comment'):
            raise Exception("Auth Error")
        author_id = RequestGetUserId(self.request)
        random_string = ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.digits) for _ in range(20))

        encoded_url = urlencode(self.request.params)
        monitor = MonitorLink(author_id=author_id,
                              link=random_string, internal_link=encoded_url)

        with transaction.manager:
            DBSession.add(monitor)

        response = {
            'link': random_string
        }

        return response

    @view_config(request_method='GET', renderer='json')
    def read(self):
        try:
            return self._get_monitor().get('data')
        except Exception as e:
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

    def _get_monitor(self):
        author_id = RequestGetUserId(self.request)
        if author_id == -1:
            return {"result": "error", "message": 'Unauthorised'}

        link = self.request.matchdict['link']

        monitor = DBSession.query(MonitorLink) \
            .filter(MonitorLink.link == link)\
            .one_or_none()

        if monitor is None:
            return {"result": "error", "message": 'Monitor is not found'}

        query_params = monitor.internal_link

        url = 'http://localhost:12346/monitor?{}'.format(query_params)

        try:
            resp = requests.get(url, timeout=30)
            context = resp.json()
        except Exception as e:
            print('Request to :12346 failed!')
            raise

        return context

    @view_config(route_name="monitor_table", renderer="pynformatics:templates/monitor.mak")
    def render(self):
        try:
            data = self._get_monitor().get('data')
        except Exception as e:
            # TODO: как это будет рендерится? мы ведь рендерим шаблон.
            #  Надо разграничить рендеринг шаблона и возвращение джейсона
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

        if data is None:
            return {"result": "error", "message": 'Something was wrong'}

        partial_score = self.request.matchdict['partial_score']
        if partial_score == 'on':
            mode = 'partial_scores_on'
        else:
            mode = 'partial_scores_off'
        r = MonitorRenderer(data, mode)
        problems, competitors, contests_table = r.render()
        return {
            'problems': problems,
            'competitors': competitors,
            'contests_table': contests_table,
        }

