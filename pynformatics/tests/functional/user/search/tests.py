from hamcrest import assert_that, has_entries, has_key, contains

from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestAPI__user_search(TestCase):
    def setUp(self):
        super(TestAPI__user_search, self).setUp()
        users = [User() for _ in range(50)]
        for u in users:
            u.username, u.deleted = 'John', False
        self.session.add_all(users)

        self.session.flush()

    def test_ok(self):
        params = {'query': 'john', 'page': '2', 'page_size': '2'}
        response = self.app.get('/search/user', params=params, status=200)
        assert_that(
            response.json,
            has_entries({
                'data': contains(
                    {'id': 5, 'username': 'John', 'lastname': None, 'firstname': None, 'email': None},
                    {'id': 6, 'username': 'John', 'lastname': None, 'firstname': None, 'email': None}
                ),
                'records_total': 50,
                'page': 2,
                'page_size': 2,
                'pages_total': 25
            })
        )

    def test_search_query_is_empty_request(self):
        params = {'query': ''}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Search query is empty'
        }))

    def test_page_not_int(self):
        params = {'query': 'john', 'page': 'a'}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Parameter "page" must be int'
        }))

    def test_page_size_not_int(self):
        params = {'query': 'john', 'page': '1', 'page_size': 'a'}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Parameter "page_size" must be int'
        }))

    def test_page_out_of_range(self):
        params = {'query': 'john', 'page': '100'}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Page number is out of range'
        }))

        params = {'query': 'john', 'page': '-1'}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Page number is out of range'
        }))

    def test_page_size_negative(self):
        params = {'query': 'john', 'page_size': '-1'}
        response = self.app.get('/search/user', params=params, status=400)
        assert_that(response.json, has_entries({
            'message': 'Page size is negative or zero'
        }))
