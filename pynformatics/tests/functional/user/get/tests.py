from hamcrest import (
    assert_that,
    has_entries,
    anything,
)


from pynformatics.testutils import TestCase
from pynformatics.model.user import User
from pynformatics.model.group import Group, UserGroup
from pynformatics.utils.exceptions import UserNotFound

from pynformatics.view.user import user_get

class TestAPI__user_get(TestCase):
    def setUp(self):
        super(TestAPI__user_get, self).setUp()

        self.user = User()
        self.user.firstname = 'Ivan'
        self.user.lastname = 'Ivanov'

        self.session.add(self.user)
        self.session.flush()

        self.groups = [Group(id=str(i), name='TestGroup' + str(i))
                       for i in range(5)]
        self.groups_dict = {group.id: group.name for group in self.groups}
        self.session.add_all(self.groups)
        self.session.flush()

        self.usergroups = [UserGroup(user_id=self.user.id,
                                     user=self.user,
                                     group_id=group.id,
                                     group=group)
                           for group in self.groups]
        self.session.add_all(self.usergroups)
        self.session.flush()


    def send_request(self, user_id, status_code=200):
        response = self.app.get(
            url='/user/{}'.format(user_id),
            status=status_code,
        )
        return response

    def test_simple(self):
        response = self.send_request(self.user.id)

        assert_that(
           response.json,
           has_entries({
               'id': self.user.id,
               'firstname': self.user.firstname,
               'lastname': self.user.lastname,
           })
        )

    def test_no_user(self):
        response = self.send_request(user_id=self.user.id + 1, status_code=404)

        assert_that(
            response.json,
            has_entries({
                'code': 404,
                'message': 'No such user',
            })
        )

    def test_user_groups(self):
        response = self.send_request(self.user.id)

        assert_that(
            response.json,
            has_entries({
                'id': self.user.id,
                'firstname': self.user.firstname,
                'lastname': self.user.lastname,
                'groups': self.groups_dict,
            })
        )


