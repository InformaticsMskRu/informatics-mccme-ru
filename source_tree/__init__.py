from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from pyramid.events import NewRequest
from sqlalchemy import engine_from_config
from source_tree.models import DBSession
import source_tree.models
from source_tree.utils.session import subscribe_rollback_on_request_finished


def course_include(config):
    config.add_route('course.get', 'get/{course_id}')
    config.add_route('course.get.children', 'get/{course_id}/children')
    config.add_route('course.add', 'add')
    config.add_route('course.erase', 'erase/{course_id}')
    config.add_route('course.erase.all', 'erase/{course_id}/all')
    config.add_route('course.update', 'update/{course_id}')
    config.add_route('course.verify', 'verify/{course_id}')
    config.add_route('course.verify.cancel', 'verify/{course_id}/cancel')
    config.add_route('course.get.all.to_verify', 'get/all/to_verify')
    config.add_route('course.adm', 'adm')
    config.add_route('course.dump', 'dump/{course_id}')
    config.add_route('course.add.window', 'add_course_window/{course_id}')
    config.add_route('course.get.nodes', 'get/{course_id}/nodes')
    config.add_route('course.get_for_select', 'get_for_select')
    config.add_route('course.my_categories', 'my_categories')
    config.add_route('course.get_not_in_list', 'get_not_in_list')
    config.add_route('course.get_by_author', 'get_by_author/{author_id}')
    config.add_route('course.verify_list', 'verify_list')
    config.add_route('course.all', 'all')


def py_source_include(config):
    config.add_static_view('img', 'static/img', cache_max_age=3600)
    config.add_static_view('js', 'static/js', cache_max_age=3600)
    config.add_static_view('html', 'static/html', cache_max_age=3600)
    config.add_static_view('css', 'static/css', cache_max_age=3600)

    config.add_route('source.add', 'source/add')
    config.add_route('source.update', 'source/update/{source_id}')
    config.add_route('source.erase', 'source/erase/{source_id}')
    config.add_route('source.erase.all', 'source/erase/{source_id}/all')
    config.add_route('source.verify', 'source/verify/{source_id}')
    config.add_route('source.verify.cancel', 'source/verify/{source_id}/cancel')
    config.add_route('source.get.children', 'source/get/{source_id}/children')
    config.add_route('source.get', 'source/get/{source_id}')
    config.add_route('source.get.all', 'source/get/all/{source_type}')
    config.add_route('source.get.all.to_verify', 'source/get/all/{source_type}/to_verify')
    config.add_route('source.adm', 'source/adm')
    config.add_route('source.adm.form', 'source/adm/form')
    config.add_route('source.dir', 'source/dir/{source_id}')
    config.add_route('source.dir.home', 'source/dir')
    config.add_route('source.dir.contest.current', 'source/dir/contest/current')
    config.add_route('source.dir.contest.get_problems', 'source/dir/contest/get_problems')
    config.add_route('source.dir.contest.add_problem', 'source/dir/contest/add_problem/{problem_id}')
    config.add_route('source.dir.contest.erase_problem', 'source/dir/contest/erase_problem/{problem_index}')
    config.add_route('source.dir.contest.move_problem', 'source/dir/contest/move_problem/{problem_index}/{move_type}')
    config.add_route('source.dir.contest.clean', 'source/dir/contest/clean')
    config.add_route('source.dir.contest.new', 'source/dir/contest/new/{contest}')
    config.add_route('source.dir.contest.create', 'source/dir/contest/create')
    config.add_route('subject.adm', 'subject/adm')

    config.add_route('problem.get.source.html', 'problem/get/{problem_id}/{source_type}/html')
    
    config.add_route('problem.set.source', 'problem/set/{problem_id}/{source_type}')
    config.add_route('problem.add.source', 'problem/add/{problem_id}/source/{subject_id}')
    config.add_route('problem.get.source', 'problem/get/{problem_id}/{source_type}')
    config.add_route('problem.get.source.to_verify', 'problem/get/{problem_id}/{source_type}/to_verify')

    config.add_route('contest.add.source', 'contest/add/{contest_id}/source/{source_id}')
    config.add_route('contest.set.source', 'contest/set/{contest_id}/source')
    
    config.add_route('access', 'access')

    config.add_route('protocol', 'protocol')

    config.add_route('home', '/')
    config.include(course_include, 'course')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    models.db_session = DBSession()

    config = Configurator(settings=settings, session_factory=UnencryptedCookieSessionFactoryConfig('source_tree_session'))
    config.include('pyramid_mako')
    config.include(py_source_include, route_prefix=settings['source_tree.route_prefix'])

    config.add_subscriber(subscribe_rollback_on_request_finished, NewRequest)

    config.scan()
    return config.make_wsgi_app()
