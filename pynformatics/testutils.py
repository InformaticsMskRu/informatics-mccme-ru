import mock
import unittest
import sys
import transaction
from beaker.session import Session
from pyramid import testing
from sqlalchemy import create_engine
from unittest.mock import PropertyMock
from webtest import TestApp

from pynformatics import main
from pynformatics.model.group import (
    Group,
    UserGroup,
)
from pynformatics.model.meta import Base
from pynformatics.model.problem import EjudgeProblem
from pynformatics.model.statement import Statement
from pynformatics.model.user import SimpleUser

# TODO: Импорт необходим, иначе не создает таблицы в тестах
from pynformatics.model.standings import (
    ProblemStandings,
    StatementStandings,
)

from pynformatics.models import DBSession
from source_tree.model.role import Role


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///', echo=False)
        engine.execute('attach database "temp/moodle.db" as moodle;')
        engine.execute('attach database "temp/ejudge.db" as ejudge;')
        engine.execute('attach database "temp/pynformatics.db" as pynformatics;')

        Base.metadata.create_all(engine)

        cls._app = main(
            {
                'TEST': True,
                'engine': engine,
            },
            **{
                'session.key': 'session',
            }
        )

        DBSession.configure(bind=engine)
        cls.session = DBSession

    @classmethod
    def tearDownClass(cls):
        DBSession.remove()

    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.app = TestApp(self._app)

        self.mock_context_check_auth = mock.patch('pynformatics.utils.context.Context.check_auth')
        self.mock_context_check_roles = mock.patch('pynformatics.utils.context.Context.check_roles')
        self.mock_context_user = mock.patch('pynformatics.utils.context.Context.user', new_callable=PropertyMock)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def get_session(self):
        session_id = self.app.cookies.get('session', None)

        # При вызове set_cookie значение всегда обрамляется кавычками, из-за чего нужен этот костыль
        # https://github.com/Pylons/webtest/issues/171
        if len(session_id) == 34:
            session_id = session_id[1:-1]
        return Session({}, id=str(session_id))

    def set_session(self, data):
        # При вызове set_cookie значение всегда обрамляется кавычками
        # https://github.com/Pylons/webtest/issues/171
        session = Session({})
        session.update(data)
        session.save()
        self.app.set_cookie('session', session.id)

    def create_groups(self):
        self.groups = [
            Group(
                name='group 1',
                visible=1,
            ),
            Group(
                name='group 2',
                visible=1,
            ),
        ]
        self.session.add_all(self.groups)
        self.session.flush(self.groups)

    def create_problems(self):
        self.problems = [
            EjudgeProblem(
                ejudge_prid=1,
                contest_id=1,
                ejudge_contest_id=1,
                problem_id=1,
            ),
            EjudgeProblem(
                ejudge_prid=2,
                contest_id=2,
                ejudge_contest_id=1,
                problem_id=2,
            ),
            EjudgeProblem(
                ejudge_prid=3,
                contest_id=3,
                ejudge_contest_id=2,
                problem_id=1,
            )
        ]
        self.session.add_all(self.problems)
        self.session.flush(self.problems)

    def create_roles(self):
        self.admin_role = Role(shortname='admin')
        self.course_creator = Role(shortname='coursecreator')
        self.teacher = Role(shortname='editingteacher')
        self.non_editing_teacher = Role(shortname='teacher')
        self.student = Role(shortname='student')
        self.guest = Role(shortname='guest')
        self.authenticated_user = Role(shortname='user')
        self.group_teacher = Role(shortname='group')
        self.ejudge_teacher = Role(shortname='ejudge')
        self.editor = Role(shortname='editor')
        self.testing = Role(shortname='testing')
        self.source_editor = Role(shortname='source_editor')
        self.course_editor = Role(shortname='course_editor')
        self.view_courses = Role(shortname='view_courses')
        self.session.add_all((
            self.admin_role, self.course_creator,
            self.teacher, self.non_editing_teacher,
            self.student, self.guest,
            self.authenticated_user, self.group_teacher,
            self.ejudge_teacher, self.editor,
            self.testing, self.source_editor,
            self.course_editor, self.view_courses
        ))

    def create_statements(self):
        self.statements = [
            Statement(),
            Statement(),
        ]
        self.session.add_all(self.statements)
        self.session.flush(self.statements)

    def create_user_groups(self):
        self.create_groups()
        self.create_users()

        self.user_groups = [
            UserGroup(
                group=self.groups[0],
                user=self.users[0],
            ),
            UserGroup(
                group=self.groups[1],
                user=self.users[1],
            ),
        ]
        self.session.add_all(self.user_groups)
        self.session.flush(self.user_groups)

    def create_users(self):
        self.users = [
            SimpleUser(
                firstname='Maxim',
                lastname='Grishkin',
                ejudge_id=179,
            ),
            SimpleUser(
                firstname='Somebody',
                lastname='Oncetoldme',
                ejudge_id=1543,
            ),
        ]
        self.session.add_all(self.users)
        self.session.flush(self.users)


def dummy_decorator(*args, **kwargs):
    return lambda func: func


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        path = 'tests'
    else:
        path = sys.argv[1]

    try:
        tests = unittest.TestLoader().discover(path)
    except:
        tests = unittest.TestLoader().loadTestsFromName(path)

    result = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
    sys.exit(not result)
