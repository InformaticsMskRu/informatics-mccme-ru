from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.model.group import Group


class TestAPI__group_get(TestCase):
    def setUp(self):
        super(TestAPI__group_get, self).setUp()
        self.create_groups()

    def send_request(self, group_id, status_code=None):
        return self.app.get(
            url='/group/%s' % group_id,
            status=status_code or 200
        )

    def test_simple(self):
        response = self.send_request(1)
        assert_that(
            response.json,
            equal_to({
                'name': 'group 1',
                'visible': 1,
                'description': None,
                'owner_id': None,
            })
        )

    def test_not_found(self):
        response = self.send_request(179, status_code=404)
        assert_that(
            response.json,
            equal_to({
                'code': 404,
                'message': 'No group with this id',
            })
        )

    def test_invisible_not_found(self):
        invisible_group = Group(visible=False)
        self.session.add(invisible_group)
        self.session.flush()

        response = self.send_request(invisible_group.id, status_code=404)
        assert_that(
            response.json,
            equal_to({
                'code': 404,
                'message': 'No group with this id',
            })
        )
