from hamcrest import (
    assert_that,
    has_entries,
    anything,
)


from pynformatics.testutils import TestCase
from pynformatics.model.user import User
from source_tree.model.role import (
    Role,
    RoleAssignment,
)


class TestAPI__user_reset_password(TestCase):
    def setUp(self):
        super(TestAPI__user_reset_password, self).setUp()

        self.create_roles()

        self.user = User()
        self.admin_user = User()
        self.session.add_all((self.user, self.admin_user))

        self.session.flush()

        role_assignment = RoleAssignment(
            role_id=self.admin_role.id,
            user_id=self.admin_user.id,
        )
        self.session.add(role_assignment)


    def send_request(self,
                     user_id=None,
                     session_user_id=None,
                     status_code=200,
                     ):
        if session_user_id:
            self.set_session({'user_id': session_user_id})
        response = self.app.post_json(
            url='/user/reset_password',
            params={
                'id': user_id,
            },
            status=status_code,
        )
        return response

    def test_simple(self):
        response = self.send_request(
            session_user_id=self.admin_user.id,
            user_id=self.user.id,
        )
        assert_that(
            response.json,
            has_entries({
                'id': self.user.id,
                'password': anything(),
            })
        )

    def test_no_user(self):
        response = self.send_request(
            session_user_id=self.admin_user.id,
            user_id='bad user id',
            status_code=404,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 404,
                'message': 'No such user',
            })
        )

    def test_not_admin(self):
        response = self.send_request(
            session_user_id=self.user.id,
            user_id=self.admin_user.id,
            status_code=403,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Forbidden',
            })
        )

    def test_not_authorized(self):
        response = self.send_request(
            user_id=self.user.id,
            status_code=401,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 401,
                'message': 'Unauthorized',
            })
        )
