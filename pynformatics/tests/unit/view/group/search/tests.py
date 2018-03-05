import mock
from hamcrest import (
    assert_that,
    contains_inanyorder,
    equal_to,
)

from pynformatics.model import Group
from pynformatics.testutils import TestCase
from pynformatics.view.group import group_search


class TestView__group_search(TestCase):
    def setUp(self):
        super(TestView__group_search, self).setUp()

        self.groups = [
            Group(name='group 1', visible=True),
            Group(name='group 2', visible=True),
            Group(name='group 3', visible=True),
            Group(name='aa', visible=True),
            Group(name='bb', visible=True),
            Group(name='cc', visible=True),
            Group(name='invisible', visible=False),
        ]
        self.session.add_all(self.groups)
        self.session.flush()

    def call_view(self, name=None):
        context_mock = mock.Mock()
        serialize_mock = mock.Mock(return_value='serialized')

        if name is not None:
            self.request.params['name'] = name

        with mock.patch.object(Group, 'serialize', serialize_mock):
            result = group_search(self.request, context_mock)

        for group_id in result:
            assert_that(result[group_id], equal_to('serialized'))

        return result

    def test_multiple(self):
        result = self.call_view('group')
        assert_that(result.keys(), contains_inanyorder(1, 2, 3))

    def test_single(self):
        result = self.call_view('group 3')
        assert_that(result.keys(), contains_inanyorder(3))

    def test_empty(self):
        result = self.call_view('abacaba')
        assert_that(result, equal_to({}))

    def test_limit_and_order(self):
        result = self.call_view()
        assert_that(result.keys(), contains_inanyorder(1, 2, 3, 4, 5))

    def test_invisible(self):
        result = self.call_view(self.groups[-1].name)
        assert_that(result, equal_to({}))
