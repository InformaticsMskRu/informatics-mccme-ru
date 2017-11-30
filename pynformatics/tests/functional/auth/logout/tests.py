from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
    calling,
    raises,
    is_not,
    has_items,
)

from pynformatics.model.user import User
from pynformatics.testutils import TestCase
from pynformatics.utils.functions import attrs_to_dict


class TestAPI__auth_logout(TestCase):
    def setUp(self):
        super(TestAPI__auth_logout, self).setUp()

        self.username = 'some username'
        self.password = 'testtest'
        self.password_md5 = '05a671c66aefea124cc08b76ea6d30bb'

        self.user = User(
            username=self.username,
            password=self.password_md5,
            firstname='some firstname',
            lastname='some lastname'
        )
        self.session.add(self.user)
        self.session.flush()

    def send_request(self,status_code=200):
        return self.app.post(
            '/auth/logout',
            status=status_code,
        )

    def check_request(self,
                      status_code=200,
                      message=None,
                      ):
        response = self.send_request(status_code)
        if status_code != 200:
            assert_that(
                response.json,
                has_entries({
                    'code': status_code,
                    'message': message,
                })
            )
            return

        assert_that(
            response.json,
            equal_to({})
        )

        # В сессии больше нет user_id
        assert_that(
            self.get_session(),
            has_entries({
                'user_id': None,
            })
        )

        # В куках сброшена сессия мудла
        assert_that(
            self.app.cookies.get('MoodleSession'),
            equal_to('')
        )

    def test_simple(self):
        self.set_session({'user_id': self.user.id})
        self.app.set_cookie('MoodleSession', 'somevalue')
        self.check_request()

    def test_logged_out(self):
        self.check_request(
            status_code=401,
            message='Unauthorized',
        )

    def test_bad_login(self):
        self.set_session({'user_id': 'bad user_id'})
        self.check_request(
            status_code=401,
            message='Unauthorized',
        )
