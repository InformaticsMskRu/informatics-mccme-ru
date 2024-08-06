import random
import string
import traceback
from typing import List, Dict

import requests
import transaction
from pyramid.encode import urlencode
from pyramid.view import view_config, view_defaults
from sqlalchemy.orm import load_only
import pyramid.httpexceptions as ex

from pynformatics.model import User, Statement
from pynformatics.model.monitor import MonitorLink
from pynformatics.models import DBSession
from pynformatics.view.monitor.monitor_renderer import MonitorRenderer
from pynformatics.view.utils import *
from pynformatics.view.utils import is_authorized_id
from pynformatics.utils.check_role import is_admin


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
    def create_secret_link(self):
        if not RequestCheckUserCapability(self.request, 'moodle/ejudge_submits:admin'):
            raise ex.HTTPForbidden()
        author_id = RequestGetUserId(self.request)
        random_string = ''.join(random.SystemRandom().choice(
            string.ascii_lowercase + string.digits) for _ in range(20))

        internal_link = urlencode(self.request.params)
        monitor = MonitorLink(author_id=author_id,
                              link=random_string, internal_link=internal_link)

        with transaction.manager:
            DBSession.add(monitor)

        response = {
            'link': random_string
        }

        return response

    @view_config(route_name="monitor_table", renderer="pynformatics:templates/monitor.mak")
    def render_as_html_by_secret_link(self):
        author_id = RequestGetUserId(self.request)
        if not is_authorized_id(author_id):
            raise ex.HTTPUnauthorized()
        link_arg = self.request.matchdict['link']
        internal_link = self._get_saved_internal_link(link_arg)
        try:
            data = self._get_monitor(internal_link).get('data')
        except Exception as e:
            # TODO: как это будет рендерится? мы ведь рендерим шаблон.
            #  Надо разграничить рендеринг шаблона и возвращение джейсона
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

        if data is None:
            return {"result": "error", "message": 'Something was wrong'}

        return self._make_template_values(data)

    @view_config(route_name='monitor_create', request_method='GET', renderer="pynformatics:templates/monitor.mak")
    @view_config(route_name='monitor_create_json', request_method='GET', renderer="json")
    def render_as_html_by_public(self):
        author_id = RequestGetUserId(self.request)
        if not is_authorized_id(author_id):
            raise ex.HTTPUnauthorized()

        try:
            cmid = int(self.request.params['contest_id'])
        except:
            return {"result": "error", "message": "wrong course id"}
        if 'group_id' in self.request.params:
            group_id = int(self.request.params['group_id'])
        else:
            group_id = None

        internal_link = urlencode(self.request.params)

        result = {}

        try:
            if group_id is None:
                result = self._get_monitor_by_user_ids(cmid, 0, internal_link, self.request)
                problems = result.get('data')
                # return {'p': problems, 'r': result}
            else:
                problems = self._get_monitor(internal_link).get('data')
        except Exception as e:
            # TODO: как это будет рендерится? мы ведь рендерим шаблон.
            #  Надо разграничить рендеринг шаблона и возвращение джейсона
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

        if problems is None:
            return {"result": "error", "message": 'Something was wrong'}

        data = {}
        data['problems'] = problems
        # Get extra info for problems' contests
        data['contests'] = self._get_contests_info(problems)
        if "user_ids" in result:
            data['user_ids'] = result["user_ids"]
        isAdmin = is_admin(self.request)
        view_settings = dict()
        view_settings["show_email"] = bool(self.request.params.get('show_email')) and isAdmin
        view_settings["show_login"] = bool(self.request.params.get('show_login')) and isAdmin
 
        return self._make_template_values(data, view_settings)

    @view_config(request_method='GET', renderer='json')
    def get_raw_json(self):
        link_arg = self.request.matchdict['link']
        internal_link = self._get_saved_internal_link(link_arg)
        try:
            return self._get_monitor(internal_link).get('data')
        except Exception as e:
            return {"result": "error", "message": str(e), "stack": traceback.format_exc()}

    def _make_template_values(self, data, view_settings = None):
        partial_score = self.request.params.get('partial_score')
        if partial_score == 'on':
            mode = 'partial_scores_on'
        else:
            mode = 'partial_scores_off'
        r = MonitorRenderer(data, mode)
        problems, competitors, contests_table, problem_attr = r.render()
        return {
            'problems': problems,
            'competitors': competitors,
            'contests_table': contests_table,
            'problem_attr': problem_attr if self.request.params.get('json') is None else None,
            'view_settings': view_settings,
            'user_ids': data["user_ids"] if "user_ids" in data else None,
        }

    @classmethod
    def _get_saved_internal_link(cls, link) -> str:
        monitor = DBSession.query(MonitorLink) \
            .filter(MonitorLink.link == link) \
            .one_or_none()

        if monitor is None:
            raise Exception('Monitor is not found')

        return monitor.internal_link

    @classmethod
    def _get_contests_info(cls, problems: List[Dict]) -> Dict:
        """Get names for problems' contests.

        Returns:

            { contest_id: 'contest_name', ... }

        :param problems: A list of problems with its' contest ids
        :return: dict with contests names, where key is contest id
        """
        # Gather unique contests ids to fetch additional info for rendering
        contests_ids = {problem.get('contest_id') for problem in problems}
        statements = DBSession.query(Statement) \
            .filter(Statement.id.in_(contests_ids)) \
            .options(load_only('id', 'name')) \
            .all()

        return {s.id: s.name for s in statements}

    def _get_monitor(self, internal_link) -> dict:
        url = '{}/monitor?{}'.format(self.request.registry.settings['rmatics.endpoint'], internal_link)

        try:
            resp = requests.get(url, timeout=30)
            context = resp.json()
        except Exception as e:
            print('Request to :12346 failed!')
            raise

        return context

    def _get_monitor_by_user_ids(self, cmid, moodle_group_id, internal_link, request) -> dict:
        url = '{}/monitor?{}'.format(self.request.registry.settings['rmatics.endpoint'], internal_link)

        try:
            user_ids = GetUserIds(request, cmid, moodle_group_id)
            resp = requests.post(url, json={"user_ids": user_ids}, timeout=30)
            context = resp.json()
            context['user_ids'] = user_ids
        except Exception as e:
            print('Request to :12346 failed!')
            raise

        return context
