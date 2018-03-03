from hamcrest import assert_that, has_entries, contains, only_contains

from pynformatics import User
from pynformatics.model import Group, UserGroup, GroupInviteLinkWithContest
from pynformatics.testutils import TestCase
from source_tree.model.role import RoleAssignment


class TestAPI__group(TestCase):
    def setUp(self):
        super(TestAPI__group, self).setUp()

        self.create_roles()

        self.teacher = User()
        self.teacher2 = User()
        self.user1 = User()
        self.user2 = User()

        self.session.add_all((
            self.teacher,
            self.teacher2,
            self.user1,
            self.user2
        ))
        self.session.flush()

        self.group = Group(owner_id=self.teacher.id, name="test_group")
        self.group2 = Group(owner_id=self.teacher2.id, name="test_group2")

        self.session.add_all((
            self.group,
            self.group2
        ))
        self.session.flush()

        self.session.add_all((
            RoleAssignment(
                user_id=self.teacher.id,
                role_id=self.admin_role.id,
            ),
            UserGroup(
                user_id=self.user1.id,
                group_id=self.group.id
            ),
            UserGroup(
                user_id=self.user2.id,
                group_id=self.group.id
            ),
        ))
        self.session.flush()

    def test_group_get(self):
        response = self.app.get("/group/1")
        assert_that(
            response.json,
            has_entries({
                'data': only_contains(
                    has_entries({
                        'id': 1,
                        'name': 'test_group',
                        'owner_id': 1
                    }),
                ),
            })
        )

    def test_group_get_owned_by(self):
        response = self.app.get("/group/owned_by/2")
        assert_that(
            response.json,
            has_entries({
                'data': only_contains(
                    has_entries({
                        'id': 2,
                        'name': 'test_group2',
                        'owner_id': 2
                    }),
                ),
            })
        )

    def test_group_add_invite_link(self):
        self.set_session({'user_id': self.teacher.id})
        response = self.app.post_json("/group/1/add_invite_link", params={
            "contest_id": 100
        })
        assert_that(
            response.json,
            has_entries({
                'id': 1,
                'group_id': 1,
                'contest_id': 100,
                'is_active': True,
                'link': '867nv'
            })
        )

    def test_group_get_invite_links(self):
        self.session.add_all((
            GroupInviteLinkWithContest(2, 100),
            GroupInviteLinkWithContest(2, 102),
        ))
        self.session.flush()
        response = self.app.get("/group/2/invite_links")
        assert_that(
            response.json,
            has_entries({
                'data': only_contains(
                    has_entries({
                        'id': 1,
                        'group_id': 2,
                        'contest_id': 100,
                        'is_active': True,
                        'link': '867nv'
                    }),
                    has_entries({
                        'id': 2,
                        'group_id': 2,
                        'contest_id': 102,
                        'is_active': True,
                        'link': '25t52'
                    }),
                ),
            })
        )
