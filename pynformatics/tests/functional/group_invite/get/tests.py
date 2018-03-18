from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.group_invite import GroupInvite
from pynformatics.testutils import TestCase


class TestAPI__group_invite_get(TestCase):
    def setUp(self):
        super(TestAPI__group_invite_get, self).setUp()
        self.create_users()
        self.create_groups()

        self.group_invite = GroupInvite(
            group=self.groups[0],
            creator=self.users[0],
            redirect_type=GroupInvite.REDIRECT_COURSE,
            instance_id=123,
        )
        self.session.add(self.group_invite)
        self.session.flush()

    def send_request(self, user=None, status=None):
        if user:
            self.set_session({
                'user_id': user.id,
            })
        response = self.app.get('/group_invite', status=status)
        return response

    def test_simple(self):
        response = self.send_request(user=self.users[0])
        assert_that(
            response.json,
            equal_to(
                [
                    {
                        'group_id': self.groups[0].id,
                        'creator_id': self.users[0].id,
                        'redirect': {'course_id': 123},
                        'disabled': False,
                        'url': 'bcacbaabcaaaabc',
                    }
                ]
            )
        )

    def test_empty(self):
        response = self.send_request(user=self.users[1])
        assert_that(response.json, equal_to([]))

    def test_unauthorized(self):
        response = self.send_request(status=401)
        assert_that(
            response.json,
            equal_to({
                'code': 401,
                'message': 'Unauthorized',
            })
        )
