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
from pynformatics.model.meta import Base
from pynformatics.models import DBSession


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

        cls.session = DBSession

    @classmethod
    def tearDownClass(cls):
        DBSession.remove()

    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()
        self.app = TestApp(self._app)

        self.mock_context_check_auth = mock.patch('pynformatics.utils.context.Context.check_auth')
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

def dummy_decorator(*args, **kwargs):
    return lambda func: func


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        tests = unittest.TestLoader().discover('tests')
    else:
        tests = unittest.TestLoader().loadTestsFromName(sys.argv[1])
    result = unittest.TextTestRunner(verbosity=2).run(tests).wasSuccessful()
    sys.exit(not result)
