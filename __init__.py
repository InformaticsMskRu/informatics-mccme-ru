from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import DBSession
from pynformatics.view.comment import *

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine, expire_on_commit=False)
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('comment.add', '/comment/add')
    config.add_route('comment.get', '/comment/get/{contest_id}/{run_id}')
    config.add_route('user_settings.add', '/user/settings/main/add')
    config.add_route('user_settings.get', '/user/settings/main/get/{user_id}')
    config.add_route('comment.get_count', '/comment/count')
    config.add_route('comment.get_all', '/comment/all')
    config.add_route('comment.get_all_html', '/comment/all/html')
    config.add_route('comment.get_all_limit', '/comment/all/{start}/{stop}')
    config.add_route('comment.get_all_limit_html', '/comment/all/{start}/{stop}/html')
    config.add_route('comment.get_unread_limit', '/comment/unread/{start}/{stop}')
    config.add_route('comment.get_unread_limit_html', '/comment/unread/{start}/{stop}/html')
    config.add_route('comment.get_count_unread', '/comment/unread/count')
    config.add_route('protocol.get', '/protocol/get/{contest_id}/{run_id}')
    config.add_route('run.rejudge', '/run/rejudge/{contest_id}/{run_id}/{status_id}')
    config.add_route('team_monitor.get', '/team_monitor/get/{statement_id}')
    config.add_route('contest.ejudge.reload.problem', '/contest/ejudge/reload/{contest_id}/{problem_id}')
    config.add_route('problem.submit', '/problem/{problem_id}/submit')
    config.add_route('problem.limits.show', '/problem/{problem_id}/limits/show')
    config.add_route('problem.limits.hide', '/problem/{problem_id}/limits/hide')
    config.add_route('problem.tests.count', '/problem/{problem_id}/tests/count')
    config.add_route('problem.generate_samples', '/problem/{problem_id}/generate_samples')
    config.add_route('problem.tests.add', '/problem/{problem_id}/tests/add')
    config.add_route('problem.tests.set_preliminary', '/problem/{problem_id}/tests/set_preliminary')
    config.add_route('problem.tests.get_test', '/problem/{problem_id}/tests/test/{test_num}')
    config.add_route('problem.tests.get_corr', '/problem/{problem_id}/tests/corr/{test_num}')
    config.add_route('contest.ejudge.reload', '/contest/ejudge/reload/{contest_id}')
    config.add_route('contest.ejudge.get_table', '/contest/ejudge/get_table')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

