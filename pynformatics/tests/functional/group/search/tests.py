from hamcrest import (
    assert_that,
    has_entries,
    equal_to,
)

from pynformatics.model.group import Group
from pynformatics.testutils import TestCase


class TestAPI__group_search(TestCase):
    def setUp(self):
        super(TestAPI__group_search, self).setUp()

        self.groups = [
            Group(name='group 1', visible=True),
            Group(name='group 2', visible=True),
            Group(name='aaaaaaa', visible=True),
            Group(name='bbbbbbb', visible=True),
            Group(name='ccccccc', visible=True),
            Group(name='ddddddd', visible=True),
        ]
        self.session.add_all(self.groups)
        self.session.flush()

    def send_request(self, name=None):
        url = '/group'
        if name is not None:
            url += '?name=' + name

        return self.app.get(url)

    def test_simple(self):
        response = self.send_request('group')
        assert_that(
            response.json,
            has_entries({
                '1': has_entries({
                    'name': 'group 1',
                }),
                '2': has_entries({
                    'name': 'group 2'
                }),
            })
        )

    def test_empty(self):
        response = self.send_request('xxxxxxx')
        assert_that(
            response.json,
            equal_to({})
        )

    def test_limit(self):
        response = self.send_request()
        assert_that(
            len(response.json.keys()),
            equal_to(5)
        )

    def test_skips_invisible(self):
        name = 'invisible'
        invisible_group = Group(name=name, visible=False)
        self.session.add(invisible_group)
        self.session.flush()

        response = self.send_request(name)
        assert_that(response.json, equal_to({}))
