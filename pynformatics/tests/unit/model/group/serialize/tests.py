import mock
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.group import Group
from pynformatics.testutils import TestCase


class TestModel__group_serialize(TestCase):
    def test_simple(self):
        self.create_users()
        group = Group(
            name='1',
            description='2',
            owner=self.users[0],
            visible=True,
        )
        self.session.add(group)
        self.session.flush()

        assert_that(
            group.serialize(mock.Mock()),
            equal_to({
                'name': '1',
                'description': '2',
                'owner_id': self.users[0].id,
                'visible': True,
            })
        )
