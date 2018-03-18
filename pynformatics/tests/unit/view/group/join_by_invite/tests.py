import mock
from hamcrest import (
    assert_that,
    calling,
    equal_to,
    raises,
)

from pynformatics.model.group import UserGroup
from pynformatics.testutils import TestCase
from pynformatics.view.group import group_join_by_invite
from pynformatics.utils.exceptions import BadRequest


class TestView__group_join_by_invite(TestCase):
    def setUp(self):
        super(TestView__group_join_by_invite, self).setUp()

        self.create_users()
        self.create_groups()

        self.context_mock = mock.Mock()
        self.context_mock.user_id = self.users[0].id
        self.context_mock.user = self.users[0]

    def call_view(self, group_invite, user_group=None):
        with mock.patch('pynformatics.view.group.GroupInvite.get_by_url', mock.Mock()) as get_by_url_mock, \
                mock.patch('pynformatics.view.group.UserGroup.create_if_not_exists', mock.Mock()) as create_if_not_exists_mock:
            get_by_url_mock.return_value = group_invite
            create_if_not_exists_mock.return_value = user_group

            result = group_join_by_invite(self.request, self.context_mock)
        return result, get_by_url_mock, create_if_not_exists_mock

    def test_group_invite_url_required(self):
        assert_that(
            calling(self.call_view).with_args(self.groups[0]),
            raises(BadRequest)
        )

    def test_simple(self):
        self.request.matchdict['group_invite_url'] = 'oij'
        group_invite_mock = mock.Mock()
        group_invite_mock.group_id = self.groups[0].id
        group_invite_mock.redirect = 'redirect'
        user_group = UserGroup(user=self.users[0], group=self.groups[0])

        result, get_by_url_mock, create_if_not_exists_mock = self.call_view(
            group_invite=group_invite_mock,
            user_group=user_group,
        )

        get_by_url_mock.assert_called_once_with('oij')
        create_if_not_exists_mock.assert_called_once_with(user_id=self.users[0].id, group_id=self.groups[0].id)
        assert_that(
            result,
            equal_to({
                'joined': True,
                'redirect': 'redirect',
            })
        )

    def test_no_join(self):
        self.request.matchdict['group_invite_url'] = 'oij'
        group_invite_mock = mock.Mock()
        group_invite_mock.group_id = self.groups[0].id
        group_invite_mock.redirect = 'redirect'

        result, get_by_url_mock, create_if_not_exists_mock = self.call_view(group_invite_mock)

        get_by_url_mock.assert_called_once_with('oij')
        create_if_not_exists_mock.assert_called_once_with(
            user_id=self.users[0].id,
            group_id=self.groups[0].id
        )
        assert_that(
            result,
            equal_to({
                'joined': False,
                'redirect': 'redirect',
            })
        )
