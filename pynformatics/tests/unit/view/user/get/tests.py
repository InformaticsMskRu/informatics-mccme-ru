from hamcrest import (
    assert_that,
    calling,
    has_entries,
    has_items,
    raises,
)

from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import UserNotFound

from pynformatics.view.user import user_get


class TestView__user_get(TestCase):
    def setUp(self):
        super(TestView__user_get, self).setUp()

        self.user = User()
        self.user.firstname = 'Ivan'
        self.user.lastname = 'Ivanov'

        self.session.add(self.user)
        self.session.flush()

    def test_simple(self):
        self.request.json_body = {
            'id': self.user.id,
        }

        response = user_get(self.request, None)

        assert_that(
            response,
            has_entries({
                'id': self.user.id,
                'firstname': self.user.firstname,
                'lastname': self.user.lastname,
            })
        )

    def test_no_user(self):
        self.request.json_body = {
            'id': self.user.id + 1,
        }

        assert_that(
            calling(user_get).with_args(self.request),
            raises(UserNotFound),
        )
