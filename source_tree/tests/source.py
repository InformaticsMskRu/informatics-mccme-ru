import unittest
import sqlalchemy
from unittest.mock import patch, MagicMock
from pyramid.paster import get_app
from webtest import TestApp

from source_tree.models import Source, StatementProblem

def get_statement_problem(rank, problem_id):
    statement_problem = StatementProblem()
    statement_problem.rank = rank
    statement_problem.problem_id = problem_id
    return statement_problem

def get_sources():
    sources = [Source(name='_source' + str(i)) for i in range(10)]
    tree = ((0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (4, 6), (6, 9), (2, 7), (2, 8))
    for parent_ind, son_ind in tree:
        sources[son_ind].parent = sources[parent_ind]
    return sources

class SourceModelTestCase(unittest.TestCase):
    def setUp(self):
        self.sources = get_sources()

    def tearDown(self):
        self.sources.clear()

    def test_get_type(self):
        self.assertEqual(self.sources[9].get_type(), 
            '_source1')

    def test_get_source_path(self):
        self.assertEqual(self.sources[9].get_source_path(), 
            ['_source' + str(i) for i in (0, 1, 4, 6, 9)])


class SourceViewTestCase(unittest.TestCase):
    def setUp(self):
        self.testapp = TestApp(get_app('dev-source.ini', 'main'))
        self.sources = get_sources()
        self.sources_orig = get_sources()
        self.change_sources = []
        patch('sqlalchemy.orm.Session.commit', MagicMock()).start()
        patch('sqlalchemy.orm.Session.add', MagicMock(side_effect=self.change_tree_side_effect)).start()
        patch('sqlalchemy.orm.Session.delete', MagicMock(side_effect=self.change_tree_side_effect)).start()
        patch('source_tree.view.source.RequestGetUserId', MagicMock(side_effect=self.get_user_id_side_effect)).start()
        patch('source_tree.view.contest.RequestGetUserId', MagicMock(side_effect=self.get_user_id_side_effect)).start()
        patch('source_tree.view.source.check_capability', MagicMock(side_effect=self.check_capability_side_effect)).start()
        patch('source_tree.view.contest.check_capability', MagicMock(side_effect=self.check_capability_side_effect)).start()

    def tearDown(self):
        self.assertEqual(len(self.change_sources), 0)
        patch.stopall()

    def change_tree_side_effect(self, source):
        source_to_erase = [ch_source for ch_source in self.change_sources 
            if (
                str(ch_source.name), 
                str(ch_source.parent_id), 
                str(ch_source.order), 
                str(ch_source.problem_id),
                str(ch_source.author),
                str(ch_source.verified)
            ) == (
                str(source.name), 
                str(source.parent_id), 
                str(source.order), 
                str(source.problem_id),
                str(source.author),
                str(source.verified)
            )
        ]
        self.assertEqual(len(source_to_erase), 1)
        self.change_sources.remove(source_to_erase[0])

    def get_user_id_side_effect(self, request):
        return 2

    def check_capability_side_effect(self, request, str):
        return 1

    def test_source_update(self):
        query = {
            'name': 'source_name',
            'parent_id': 3, 
            'order': 1000,
            'problem_id': 166,    
            'author': 2
        }
        fields = ['name', 'parent_id', 'order', 'problem_id', 'author']
        with patch('sqlalchemy.orm.query.Query.one', MagicMock(return_value=self.sources[1])):
            self.testapp.get('/source/update/5', query, status=200)

        self.assertEqual(len(self.sources), len(self.sources_orig))
        for i in range(len(self.sources)):
            for key in query:
                self.assertIn(key, fields)
                if i == 1:
                    self.assertEqual(str(self.sources[i].__dict__[key]), str(query[key]))    
                else:
                    self.assertEqual(str(self.sources[i].__dict__[key]), str(self.sources_orig[i].__dict__[key]))

    def test_source_erase(self):
        self.change_sources = [self.sources[1]]
        with patch('sqlalchemy.orm.query.Query.one', MagicMock(return_value=self.sources[1])):
            self.testapp.get('/source/erase/5', status=200)

    def test_source_erase_all(self):
        self.change_sources = [self.sources[i] for i in (2, 7, 8)]
        with patch('sqlalchemy.orm.query.Query.one', MagicMock(return_value=self.sources[2])):
            self.testapp.get('/source/erase/5/all', status=200)

    def test_source_add(self):
        self.change_sources = [Source(
            name='source_add', 
            parent_id=2, 
            order=1000, 
            problem_id=1,
            author=2,
            verified=True
        )]
        query = {
            'name': 'source_add',
            'parent_id': 2,
            'order': 1000,
            'problem_id': 1
        }
        self.testapp.get('/source/add', query, status=200)

    def test_contest_add_source(self):
        self.change_sources = [Source(
            name='Задача ' + chr(ord('A') - 1 + i), 
            parent_id=5, 
            order=i * 10**7,
            author=2, 
            problem_id=i,
            verified=True
        ) for i in range(1, 4)]
        statement_problems = [get_statement_problem(rank, problem) for rank, problem in ((1, 1), (2, 2), (5, 3))]
        with patch('sqlalchemy.orm.query.Query.all', MagicMock(return_value=statement_problems)):
            self.testapp.get('/contest/add/5/source/5', {}, status=200)

    def test_source_verify(self):
        self.sources[1].verified = False
        self.testapp.get('/source/verify/1', {}, status=200)
        self.assertTrue(self.sources[1])

    def test_source_verify_cancel(self):
        self.sources[1].verified = False
        self.change_sources = [self.sources[1]]
        with patch('sqlalchemy.orm.query.Query.one', MagicMock(return_value=self.sources[1])):
            self.testapp.get('/source/verify/1/cancel', {}, status=200)
            
