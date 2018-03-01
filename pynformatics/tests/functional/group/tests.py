from hamcrest import assert_that, has_entries, contains, only_contains

from pynformatics import User
from pynformatics.model import Group, UserGroup
from pynformatics.testutils import TestCase
from source_tree.model.role import RoleAssignment


class TestAPI__group_get_owned(TestCase):
    def setUp(self):
        super(TestAPI__group_get_owned, self).setUp()

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

    def test_simple(self):
        self.set_session({'user_id': self.teacher.id})
        response = self.app.get("/group/get/owned")
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
