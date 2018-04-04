from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
)

from pynformatics.model.group import UserGroup
from pynformatics.model.group_invite import GroupInvite
from pynformatics.testutils import TestCase


class TestAPI__group_join_by_invite(TestCase):
    def setUp(self):
        super(TestAPI__group_join_by_invite, self).setUp()

        self.create_groups()
        self.create_users()

        self.creator = self.users[0]
        self.group = self.groups[0]
        self.user = self.users[1]

        self.group_invite = GroupInvite(
            group=self.group,
            creator=self.creator,
            redirect_type=GroupInvite.REDIRECT_STATEMENT,
            instance_id=123,
        )
        self.session.add(self.group_invite)
        self.session.flush()

    def test_adds_to_group(self):
        self.set_session({
            'user_id': self.user.id,
        })
        assert_that(self.user.user_groups, equal_to([]))
        self.app.post(f'/group/join/{self.group_invite.url}')
        self.session.refresh(self.user)
        assert_that(self.user.user_groups[0].group, equal_to(self.group))

    def test_ignores_if_added(self):
        self.set_session({
            'user_id': self.user.id,
        })
        response1 = self.app.post(f'/group/join/{self.group_invite.url}')
        response2 = self.app.post(f'/group/join/{self.group_invite.url}')
        self.session.flush()

        assert_that(
            response1.json,
            has_entries({'joined': True})
        )
        assert_that(
            response2.json,
            has_entries({'joined': False})
        )
        assert_that(self.session.query(UserGroup).count(), equal_to(1))


    def test_statement_redirect(self):
        self.set_session({
            'user_id': self.user.id,
        })
        response = self.app.post(f'/group/join/{self.group_invite.url}')
        assert_that(
            response.json,
            equal_to({
                'joined': True,
                'redirect': {
                    'statement_id': 123
                },
            })
        )

    def test_course_redirect(self):
        self.group_invite.redirect_type = GroupInvite.REDIRECT_COURSE
        self.session.flush()

        self.set_session({
            'user_id': self.user.id,
        })
        response = self.app.post(f'/group/join/{self.group_invite.url}')
        assert_that(
            response.json,
            equal_to({
                'joined': True,
                'redirect': {
                    'course_id': 123
                },
            })
        )

    def test_bad_group_invite_url(self):
        self.set_session({
            'user_id': self.user.id,
        })
        response = self.app.post('/group/join/badurl', status=404)
        assert_that(
            response.json,
            equal_to({
                'code': 404,
                'message': 'Group not found'
            })
        )

    def test_auth_required(self):
        response = self.app.post(f'/group/join/{self.group_invite.url}', status=401)
        assert_that(
            response.json,
            equal_to({
                'code': 401,
                'message': 'Unauthorized'
            })
        )
