from hamcrest import (
    assert_that,
    calling,
    raises,
)
from mock import mock

from pynformatics.utils.exceptions import (
    BadRequest,
    SearchQueryIsEmpty,
    PaginationPageOutOfRange,
    PaginationPageSizeNegativeOrZero
)
from pynformatics.view.search import search_user

from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestView__user_search(TestCase):
    def setUp(self):
        super(TestView__user_search, self).setUp()
        users = [User() for _ in range(50)]
        for u in users:
            u.username, u.deleted = 'John', False
        self.session.add_all(users)

        self.session.flush()

    def test_ok(self):
        with mock.patch(
                'pynformatics.model.user.User.search_by_string',
                mock.Mock(return_value=self.session.query(User))
        ) as mock_search_by_string:
            self.request.params = {'query': 'john'}
            search_user(self.request)
            mock_search_by_string.assert_called_once_with('john')

    def test_search_query_is_empty_request(self):
        self.request.params = {'query': ''}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(SearchQueryIsEmpty)
        )

    def test_page_not_int(self):
        self.request.params = {'query': 'john', 'page': 'a'}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(BadRequest, 'Parameter "page" should be int')
        )

    def test_page_size_not_int(self):
        self.request.params = {'query': 'john', 'page': '1', 'page_size': 'a'}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(BadRequest, 'Parameter "page_size" should be int')
        )

    def test_page_out_of_range(self):
        self.request.params = {'query': 'john', 'page': '100'}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(PaginationPageOutOfRange)
        )
        self.request.params = {'query': 'john', 'page': '-1'}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(PaginationPageOutOfRange)
        )

    def test_page_size_negative(self):
        self.request.params = {'query': 'john', 'page_size': '-1'}
        assert_that(
            calling(search_user).with_args(self.request),
            raises(PaginationPageSizeNegativeOrZero)
        )
