from hamcrest import (
    assert_that,
    contains_inanyorder,
    equal_to,
)

from pynformatics.contest.ejudge.submit_queue import queue_submit
from pynformatics.testutils import TestCase


class TestAPI__submit_get(TestCase):
    def setUp(self):
        super(TestAPI__submit_get, self).setUp()

        self.create_problems()
        self.create_users()
    
    def send_request(self, user_id=None, status=200):
        if user_id:
            self.set_session({'user_id': user_id})
        response = self.app.get('/submit', status=status)
        return response
    
    def test_simple(self):
        self.set_session({'user_id': self.users[0].id})
        response = self.app.post(
            url=f'/problem/{self.problems[0].id}/submit_v2',
            params={'lang_id': 27},
            upload_files=[
                ('file', 'some_file_name', b'some code'),
            ]
        )
        response = self.app.post(
            url=f'/problem/{self.problems[1].id}/submit_v2',
            params={'lang_id': 24},
            upload_files=[
                ('file', 'some_file_name', b'perl submit'),
            ]
        )

        response = self.send_request(user_id=self.users[0].id)
        assert_that(
            response.json,
            contains_inanyorder(
                {
                    'id': 1,
                    'user_id': self.users[0].id,
                    'problem_id': self.problems[0].id,
                    'source': 'some code',
                    'language_id': 27,
                },
                {
                    'id': 2,
                    'user_id': self.users[0].id,
                    'problem_id': self.problems[1].id,
                    'source': 'perl submit',
                    'language_id': 24,
                }
            )
        )
    
    def test_empty(self):
        response = self.send_request(user_id=self.users[0].id)
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
