from hamcrest import (
    assert_that,
    has_entries,
)

from pynformatics.model import Group
from pynformatics.model.group import UserGroup
from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestAPI__group_get_group(TestCase):

    def setUp(self):
        super(TestAPI__group_get_group, self).setUp()

        self.user = User()
        self.user.firstname = 'Dmitry'
        self.user.lastname = 'Galuza'
        self.session.add(self.user)
        self.session.flush()

        self.group = Group()
        self.group.name = 'Ice Floe Travelers'
        self.group.description = 'Group for those who like to travel on ice floe'
        self.group.owner_id = self.user.id
        self.session.add(self.group)
        self.session.flush()

        self.users = [User() for _ in range(10)]
        for u in self.users:
            u.firstname, u.lastname = 'Dmitry', 'Galuza'
        self.session.add_all(self.users)
        self.session.flush()

        user_groups = [UserGroup() for _ in range(10)]
        for i in range(10):
            ug = user_groups[i]
            ug.group_id = self.group.id
            ug.user_id = self.users[i].id
        self.session.add_all(user_groups)
        self.session.flush()

    def send_request(self, group_id, status_code=200):
        return self.app.get(
            url='/group/{}'.format(group_id),
            status=status_code
        )

    def test_simple(self):
        response = self.send_request(self.group.id)
        assert_that(
            response.json,
            has_entries({
                'id': self.group.id,
                'name': self.group.name,
                'description': self.group.description,
                'visible': self.group.visible
            })
        )

    def test_no_group(self):
        response = self.send_request(group_id=self.group.id + 1, status_code=404)
        assert_that(
            response.json,
            has_entries({
                'code': 404,
                'message': 'No group with this id',
            })
        )
