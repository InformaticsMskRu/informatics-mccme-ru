import mock
import unittest
import sys
import transaction
from pyramid import testing
from sqlalchemy import create_engine, MetaData, event
from unittest.mock import PropertyMock
from webtest import TestApp

from pynformatics import main
from pynformatics.model.meta import Base
from pynformatics.models import DBSession


class TestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///', echo=False)
        engine.execute('attach database "moodle.db" as moodle;')
        engine.execute('attach database "ejudge.db" as ejudge;')

        Base.metadata.create_all(engine)

        app = main({
            'TEST': True,
            'engine': engine
        })
        cls.app = TestApp(app)

        cls.session = DBSession

    @classmethod
    def tearDownClass(cls):
        DBSession.remove()

    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()

        self.mock_context_check_auth = mock.patch('pynformatics.utils.context.Context.check_auth')
        self.mock_context_user = mock.patch('pynformatics.utils.context.Context.user', new_callable=PropertyMock)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()


def dummy_decorator(*args, **kwargs):
    return lambda func: func


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        tests = unittest.TestLoader().discover('tests')
    else:
        tests = unittest.TestLoader().loadTestsFromName(sys.argv[1])
    unittest.TextTestRunner(verbosity=2).run(tests)
