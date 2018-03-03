from hamcrest import assert_that, has_items, has_entries, equal_to

from pynformatics import User
from pynformatics.model import Group, UserGroup, GroupInviteLink, Statement
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
            RoleAssignment(
                user_id=self.teacher2.id,
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

    def test_invite_get(self):
        self.set_session({'user_id': self.user1.id})
        invite = GroupInviteLink(group_id=2, redirect_type='STATEMENT', redirect_id=1)
        self.session.add_all((
            invite,
            Statement(id=1)
        ))
        self.session.flush()
        responce = self.app.get('/invite/' + invite.get_link())
        assert_that(responce.json, has_entries({
            'redirect': has_entries({'type': "STATEMENT", 'id': 1}),
            'group': has_entries({
                'id': 2,
                'name': 'test_group2',
                'owner_id': 2
            })
        }))
        assert_that(
            self.session.query(UserGroup).filter(UserGroup.group_id==2).count(),
            equal_to(1)
        )
