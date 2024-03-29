import json

class Competitor:
    """Участник соревнования"""

    def __init__(self, competitor_id, first_name, last_name, username, email, stat=None):
        self.id = competitor_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.problem_results = {}
        self.total_score = 0
        self.total_solved = 0
        self.stat = stat

    def __json__(self, _):
        return {
             "id": self.id,
             "username": self.username,
             # "name": "{} {}".format(self.first_name, self.last_name)
        }

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def sum(self):
        return self.stat.sum(self)

    def full_stat_by_prob(self, problem):
        return (
            self.get_stat_by_problem(problem),
            self.problem_status(problem),
        )

    def get_stat_by_problem(self, problem):
        return self.stat.get_stat_by_problem(self, problem)

    def problem_status(self, problem):
        return self.stat.problem_status(self, problem)

    def add_problem_result(self, problem, problem_result):
        self.problem_results[problem] = problem_result
        if not problem_result.was_seen:
            self.total_score += problem_result.score
            self.total_solved += problem_result.is_solved
