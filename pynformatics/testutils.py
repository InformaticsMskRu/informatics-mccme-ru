import unittest
from pyramid import testing
from webtest import TestApp
from pynformatics import main


class TestCase(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.request = testing.DummyRequest()

    def tearDown(self):
        testing.tearDown()


def dummy_decorator(*args, **kwargs):
    return lambda func: func
