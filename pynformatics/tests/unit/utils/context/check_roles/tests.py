from hamcrest import (
    assert_that,
    anything,
    calling,
    is_not,
    raises,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.context import Context
from pynformatics.utils.exceptions import (
    Forbidden,
)
from source_tree.model.role import (
    Role,
    RoleAssignment,
)


class TestUtils__context_check_roles(TestCase):
    def setUp(self):
        super(TestUtils__context_check_roles, self).setUp()

        self.user_id = 123

        self.role = Role(
            shortname='some role',
        )
        self.session.add(self.role)

        self.session.flush()

        self.role_assignment = RoleAssignment(
            user_id=self.user_id,
            role_id=self.role.id,
        )
        self.session.add(self.role_assignment)

        self.request.session = {
            'user_id': 123,
        }

    def test_ok(self):
        context = Context(self.request)
        assert_that(
            calling(context.check_roles).with_args(self.role.shortname),
            is_not(raises(anything))
        )

        context = Context(self.request)
        assert_that(
            calling(context.check_roles).with_args((self.role.shortname, 'some other role')),
            is_not(raises(anything))
        )

    def test_forbidden(self):
        context = Context(self.request)
        assert_that(
            calling(context.check_roles).with_args('other role'),
            raises(Forbidden)
        )

        assert_that(
            calling(context.check_roles).with_args(('other role', 'other role 2')),
            raises(Forbidden)
        )
