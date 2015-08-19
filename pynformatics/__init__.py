from pyramid.config import Configurator

from .models import DBSession
from pynformatics.view.comment import *
from sqlalchemy import engine_from_config

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine, expire_on_commit=False)
    config = Configurator(settings=settings)
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
    config.add_route('protocol.get_full', '/protocol/get-full/{contest_id}/{run_id}')
    config.add_route('protocol.get_test', '/protocol/get_test/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_corr', '/protocol/get_corr/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_outp', '/protocol/get_output/{contest_id}/{run_id}/{test_num}')
    config.add_route('protocol.get_submit_archive', '/protocol/get_submit_archive/{contest_id}/{run_id}')
    
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
    config.add_route('problem.ant.submit', '/problem-ant/{problem_id}/submit')
    
    config.add_route('contest.ejudge.reload', '/contest/ejudge/reload/{contest_id}')
    config.add_route('contest.ejudge.get_table', '/contest/ejudge/get_table')
    
    config.add_route('region.submit', '/region/res')
    config.add_route('region.submit_test', '/region/res_test')
    
    config.add_route('rating.get', '/rating/get')
    
    config.add_route('user.query', '/myuser')
    
    config.add_route('home', '/')
    
    config.add_route('hint.get', '/hint/get')
    config.add_route('hint.get_html', '/hint/get_html')
    config.add_route('hint.get_by_problem', '/hint/get_by_problem')
    config.add_route('hint.get_by_problem_html', '/hint/get_by_problem_html')
    config.add_route('hint.get_run', '/hint/get_run')
    config.add_route('hint.add', '/hint/add')
    config.add_route('hint.add_page', '/hint/add_page')

    config.add_route('recommendation.get', '/recommendation/get')
    config.add_route('recommendation.get_html', '/recommendation/get_html')
    
    config.scan()
    return config.make_wsgi_app()

