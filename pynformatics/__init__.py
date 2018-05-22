import logging
from logging.config import fileConfig

from gevent import monkey
from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from pynformatics.models import DBSession
from pynformatics.utils.oauth import fill_oauth_config_secrets
from pynformatics.utils.redis import init_redis
from pynformatics.utils.url_encoder import init_url_encoder
from pynformatics.view.comment import *

log = logging.getLogger(__name__)
monkey.patch_all()


SCAN_IGNORE = ['pynformatics.tests', 'pynformatics.testutils']


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'logging.config' in settings:
        fileConfig(settings['logging.config'], disable_existing_loggers=False)

    if global_config.get('TEST'):
        engine = global_config.get('engine')
    else:
        engine = engine_from_config(settings, 'sqlalchemy.')

    DBSession.configure(bind=engine, expire_on_commit=False)

    config = Configurator(settings=settings)

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.include('pyramid_mako')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('stars.add', '/stars/add')
    config.add_route('stars.delete', '/stars/delete')
    config.add_route('stars.get_by_user_id', '/stars/get_by_user_json')
    config.add_route('stars.get_by_user_id_html', '/stars/all')

    config.add_route('lamp.color', '/lamp/color')
    config.add_route('lamp.color_html', '/lamp/color_html')
    config.add_route('ideal.add_form', '/ideal/add_form')
    config.add_route('ideal.add', '/ideal/add')
    config.add_route('ideal.top', '/ideal/top')
    config.add_route('ideal.top_html', '/ideal/top_html')
    config.add_route('ideal.approve', '/ideal/approve')
    config.add_route('ideal.get_by_problem', '/ideal/get_by_problem')
    config.add_route('ideal.get_by_problem_html', '/ideal/get_by_problem_html')
    config.add_route('ideal.suggested', '/ideal/suggested')
    config.add_route('ideal.suggested_html', '/ideal/suggested_html')

    config.add_route('user_settings.add', '/user/settings/main/add')
    config.add_route('user_settings.get', '/user/settings/main/get/{user_id}')
    config.add_route('user.set_oauth_id', '/user/set_oauth_id')
    config.add_route('user.reset_password', '/user/reset_password')

    config.add_route('comment.add', '/comment/add')
    config.add_route('comment.get', '/comment/get/{contest_id}/{run_id}')
    config.add_route('comment.get_count', '/comment/count')
    config.add_route('comment.get_all', '/comment/all')
    config.add_route('comment.get_all_html', '/comment/all/html')
    config.add_route('comment.get_all_limit', '/comment/all/{start}/{stop}')
    config.add_route('comment.get_all_limit_html', '/comment/all/{start}/{stop}/html')
    config.add_route('comment.get_unread_limit', '/comment/unread/{start}/{stop}')
    config.add_route('comment.get_unread_limit_html', '/comment/unread/{start}/{stop}/html')
    config.add_route('comment.get_count_unread', '/comment/unread/count')

    config.add_route('protocol.get', '/protocol/get/{contest_id}/{run_id}')
    config.add_route('protocol.get_v2', '/protocol/get_v2/{contest_id}/{run_id}')
    config.add_route('protocol.get_full', '/protocol/get-full/{contest_id}/{run_id}')
    config.add_route('protocol.get_test', '/protocol/get_test/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_corr', '/protocol/get_corr/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_outp', '/protocol/get_output/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_submit_archive', '/protocol/get_submit_archive/{contest_id}/{run_id}')

    config.add_route('run.rejudge', '/run/rejudge/{contest_id}/{run_id}/{status_id}')

    config.add_route('team_monitor.get', '/team_monitor/get/{statement_id}')

    config.add_route('contest.ejudge.reload.problem', '/contest/ejudge/reload/{contest_id}/{problem_id}')

    config.add_route('problem.generate_samples', '/problem/{problem_id}/generate_samples')
    config.add_route('problem.get', '/problem/{problem_id}')
    config.add_route('problem.limits.show', '/problem/{problem_id}/limits/show')
    config.add_route('problem.limits.hide', '/problem/{problem_id}/limits/hide')
    config.add_route('problem.runs', '/problem/{problem_id}/runs')
    # config.add_route('problem.standings', '/problem/{problem_id}/standings')
    config.add_route('problem.submit', '/problem/{problem_id}/submit')
    config.add_route('problem.submit_v2', '/problem/{problem_id}/submit_v2')
    config.add_route('problem.tests.add', '/problem/{problem_id}/tests/add')
    config.add_route('problem.tests.count', '/problem/{problem_id}/tests/count')
    config.add_route('problem.tests.get_corr', '/problem/{problem_id}/tests/corr/{test_num}')
    config.add_route('problem.tests.get_test', '/problem/{problem_id}/tests/test/{test_num}')
    config.add_route('problem.tests.set_preliminary', '/problem/{problem_id}/tests/set_preliminary')
    config.add_route('problem.ant.submit', '/problem-ant/{problem_id}/submit')

    config.add_route('contest.ejudge.reload', '/contest/ejudge/reload/{contest_id}')
    config.add_route('contest.ejudge.get_table', '/contest/ejudge/get_table')
    config.add_route('contest.ejudge.statistic', '/contest/ejudge/statistic')
    config.add_route('contest.ejudge.clone', '/contest/ejudge/clone/{contest_id}')

    config.add_route('region.submit', '/region/res')
    config.add_route('region.submit_test', '/region/res_test')

    config.add_route('rating.get', '/rating/get')

    config.add_route('user.query', '/myuser')

    config.add_route('search.user', '/search/user')

    config.add_route('home', '/')

    config.add_route('hint.get', '/hint/get')
    config.add_route('hint.get_html', '/hint/get_html')
    config.add_route('hint.get_by_problem', '/hint/get_by_problem')
    config.add_route('hint.get_by_problem_html', '/hint/get_by_problem_html')
    config.add_route('hint.get_run', '/hint/get_run')
    config.add_route('hint.add', '/hint/add')
    config.add_route('hint.delete', '/hint/delete')
    config.add_route('hint.add_page', '/hint/add_page')

    config.add_route('recommendation.get', '/recommendation/get')
    config.add_route('recommendation.get_html', '/recommendation/get_html')

    config.add_route('submit.get', '/submit')

    config.add_route('statement.get_by_course_module', '/statement')
    config.add_route('statement.get', '/statement/{statement_id}')
    config.add_route('statement.set_settings', '/statement/{statement_id}/set_settings')
    config.add_route('statement.start_virtual', '/statement/{statement_id}/start_virtual')
    config.add_route('statement.finish_virtual', '/statement/{statement_id}/finish_virtual')
    config.add_route('statement.standings', '/statement/{statement_id}/standings')
    config.add_route('statement.start', '/statement/{statement_id}/start')
    config.add_route('statement.finish', '/statement/{statement_id}/finish')

    config.add_route('bootstrap', '/bootstrap')

    config.add_route('auth.login', 'auth/login')
    config.add_route('auth.logout', 'auth/logout')
    config.add_route('auth.oauth_login', 'auth/oauth_login')

    config.add_route('notification.update_run', 'notification/update_run')

    config.add_route('group.get', 'group/{group_id}')
    config.add_route('group.search', 'group')
    config.add_route('group.join_by_invite', 'group/join/{group_invite_url}')

    config.add_route('group_invite.get', 'group_invite')

    config.add_route('problem_request.create', '/problem_request')

    config.add_route('problem_requests.get', '/problem_requests')
    config.add_route('problem_request.get', '/problem_request/{problem_request_id}')

    config.add_route('problem_request.decline', '/problem_request/{problem_request_id}/decline')
    config.add_route('problem_request.approve', '/problem_request/{problem_request_id}/approve')


    try:
        import uwsgi
        config.add_route('websocket', 'websocket')
    except ImportError:
        log.error('UWSGI is not imported. Websockets will not work!')
        SCAN_IGNORE.append('pynformatics.view.websocket')


    fill_oauth_config_secrets(settings)
    init_url_encoder(settings)
    init_redis(settings)

    config.scan(ignore=SCAN_IGNORE)

    return config.make_wsgi_app()

