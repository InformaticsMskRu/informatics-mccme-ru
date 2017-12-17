from hamcrest import assert_that, equal_to

from pynformatics.model.user import User
from pynformatics.testutils import TestCase


class TestModel__user_search(TestCase):
    def setUp(self):
        super(TestModel__user_search, self).setUp()
        self.u1, self.u2, self.u3 = [User() for _ in range(3)]
        self.u1.firstname, self.u1.lastname = 'JohnSr', 'DoeSr'
        self.u2.email = 'john@john.john'
        self.u3.username = 'edoed'
        self.u1.deleted = False
        self.u2.deleted = False
        self.u3.deleted = False

        self.session.add_all((self.u1, self.u2, self.u3))

        self.session.flush()

    def test_email(self):
        assert_that(User.search_by_string('john@john').count(), equal_to(1))

    def test_username(self):
        assert_that(User.search_by_string('edoed').count(), equal_to(1))

    def test_firstname(self):
        assert_that(User.search_by_string('johnsr').count(), equal_to(1))

    def test_lastname(self):
        assert_that(User.search_by_string('doesr').count(), equal_to(1))

    def test_firstname_and_lastname(self):
        assert_that(User.search_by_string('johnsr doesr').count(), equal_to(1))

    def test_firstname_and_lastname_reversed(self):
        assert_that(User.search_by_string('doesr johnsr').count(), equal_to(1))

    def test_substring(self):
        assert_that(User.search_by_string('doe').count(), equal_to(2))

    def test_deleted(self):
        self.u1.deleted = True
        assert_that(User.search_by_string('John').count(), equal_to(1))
        assert_that(User.search_by_string('Doe').count(), equal_to(1))
