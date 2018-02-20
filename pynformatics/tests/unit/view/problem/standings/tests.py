import mock
from hamcrest import (
    assert_that,
    calling,
    raises,
)

from pynformatics.model.standings import ProblemStandings
from pynformatics.testutils import TestCase
from pynformatics.utils.exceptions import ProblemNotFound
from pynformatics.view.problem import problem_standings


class TestView__problem_standings(TestCase):
    def setUp(self):
        super(TestView__problem_standings, self).setUp()

        self.create_problems()

    def call_view(self,
                  problem_id=1,
                  create_called=False,
                  ):
        self.request.matchdict['problem_id'] = problem_id
        with mock.patch('pynformatics.model.standings.ProblemStandings.create', mock.Mock()) as create_mock:
            result = problem_standings(self.request, None)

        if create_called:
            create_mock.assert_called_once_with(problem_id=problem_id)
        else:
            create_mock.assert_not_called()

        return result

    def test_creates_if_nonexistent(self):
        self.call_view(create_called=True)

    def test_simple(self):
        ProblemStandings.create(problem=self.problems[0])
        self.call_view(create_called=False)

    def test_not_found(self):
        self.request.matchdict['problem_id'] = 123
        assert_that(
            calling(problem_standings).with_args(self.request, None),
            raises(ProblemNotFound)
        )
