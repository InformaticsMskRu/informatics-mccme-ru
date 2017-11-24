import time
from hamcrest import (
    assert_that,
    equal_to,
    has_entries,
)

from pynformatics.model.user import SimpleUser
from pynformatics.model.virtual_participant import VirtualParticipant
from pynformatics.testutils import TestCase


class TestAPI__bootstrap(TestCase):
    def setUp(self):
        super(TestAPI__bootstrap, self).setUp()

        self.user = SimpleUser(
            id=1,
            firstname='Firstname',
            lastname='Lastname',
        )
        self.session.add(self.user)

    def test_simple(self):
        with self.mock_context_check_auth, \
                self.mock_context_user as mock_context_user:
            mock_context_user.return_value = self.user
            response = self.app.get('/bootstrap')

        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.json,
            has_entries({
                'user': {
                    'id': self.user.id,
                    'firstname': self.user.firstname,
                    'lastname': self.user.lastname,
                }
            })
        )

    def test_with_active_virtual(self):
        virtual_participant = VirtualParticipant(
            user_id=self.user.id,
            statement_id=123,
            start=int(time.time()),
            duration=456,
        )
        self.session.add(virtual_participant)

        with self.mock_context_check_auth, \
                self.mock_context_user as mock_context_user:
            mock_context_user.return_value = self.user
            response = self.app.get('/bootstrap')

        assert_that(response.status_code, equal_to(200))
        assert_that(
            response.json,
            has_entries({
                'user': has_entries({
                    'active_virtual': {
                        'start': virtual_participant.start,
                        'duration': virtual_participant.duration,
                        'statement_id': virtual_participant.statement_id,
                    }
                }),
            })
        )
