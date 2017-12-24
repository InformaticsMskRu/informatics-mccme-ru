from hamcrest import (
    assert_that,
    has_entries,
)

from pynformatics.testutils import TestCase
from pynformatics.model.statement import Statement
from pynformatics.model.user import User
from source_tree.model.role import RoleAssignment


class TestAPI__statement_set_settings(TestCase):
    def setUp(self):
        super(TestAPI__statement_set_settings, self).setUp()

        self.create_roles()

        self.user = User()
        self.admin_user = User()

        self.statement = Statement()

        self.session.add_all((
            self.user,
            self.admin_user,
            self.statement,
        ))
        self.session.flush()

        role_assignment = RoleAssignment(
            user_id=self.admin_user.id,
            role_id=self.admin_role.id,
        )
        self.session.add(role_assignment)

    def send_request(self,
                     statement_id=None,
                     settings=None,
                     status_code=200,
                     user=None,
                     ):
        if user:
            self.set_session({'user_id': user.id})
        response = self.app.post_json(
            '/statement/%s/set_settings' % statement_id,
            settings,
            status=status_code,
        )
        return response

    def test_simple(self):
        settings = {
            'allowed_languages': [1, 2],
        }
        response = self.send_request(
            statement_id=self.statement.id,
            settings=settings,
            user=self.admin_user,
        )
        assert_that(
            response.json,
            has_entries({}),
        )

    def test_validation_error(self):
        settings = {
            'allowed_languages': 1,
        }
        response = self.send_request(
            statement_id=self.statement.id,
            settings=settings,
            status_code=400,
            user=self.admin_user,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 400,
                'message': '1 is not of type \'array\'',
            }),
        )

    def test_unauthorized(self):
        response = self.send_request(
            statement_id=self.statement.id,
            status_code=401,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 401,
                'message': 'Unauthorized',
            })
        )

    def test_forbidden(self):
        response = self.send_request(
            statement_id=self.statement.id,
            status_code=403,
            user=self.user,
        )
        assert_that(
            response.json,
            has_entries({
                'code': 403,
                'message': 'Forbidden',
            })
        )
