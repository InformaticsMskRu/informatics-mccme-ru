import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)

from pynformatics.model.group import Group
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import GroupNotFound
from pynformatics.view.group import group_get


class TestView__group_get(TestCase):
    def setUp(self):
        super(TestView__group_get, self).setUp()

        self.create_groups()

    def call_view(self, group_id):
        self.request.matchdict = {
            'group_id': group_id,
        }
        serialize_mock = mock.Mock(return_value='serialized')
        context_mock = mock.Mock()
        with mock.patch.object(Group, 'serialize', serialize_mock):
            result = group_get(self.request, context_mock)

        serialize_mock.assert_called_once_with(context_mock)
        assert_that(result, equal_to('serialized'))

        return result

    def test_simple(self):
        self.call_view(1)

    def test_not_found(self):
        assert_that(
            calling(self.call_view).with_args(123),
            raises(GroupNotFound)
        )
