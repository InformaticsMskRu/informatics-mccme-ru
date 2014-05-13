import unittest
import sqlalchemy
from unittest.mock import patch, MagicMock
from pyramid.paster import get_app
from webtest import TestApp

from source_tree.models import Problem, Source
from source_tree.tests.source import get_sources

class ProblemViewTestCase(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(get_app('dev-source.ini', 'main'))

    def tearDown(self):
        pass

    def test_problem_get_source_html(self):
        sources = get_sources()
        query_sources = [sources[i] for i in (9, 7)]
        correct_source_list = [
            ['_source' + str(i) for i in (0, 1, 4, 6, 9)]
        ]
        def template_render_side_effect(source_list, source_type):
            self.assertEqual(correct_source_list, source_list)
            return 'AAA!'

        with patch('sqlalchemy.orm.query.Query.all', MagicMock(return_value=query_sources)), \
                patch('mako.template.Template.render', MagicMock(side_effect=template_render_side_effect)):
            self.testapp.get('/problem/get/5/source1/html', status=200)
        
