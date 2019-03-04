class Competitor:
    """Участник соревнования"""

    def __init__(self, competitor_id, first_name, last_name, stat=None):
        self.id = competitor_id
        self.first_name = first_name
        self.last_name = last_name
        self.problem_results = {}
        self.total_score = 0
        self.total_solved = 0
        self.stat = stat

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def sum(self):
        return self.stat.sum(self)

    def full_stat_by_prob(self, problem):
        return (
            self.get_stat_by_problem(problem),
            self.is_problem_solved(problem),
        )

    def get_stat_by_problem(self, problem):
        return self.stat.get_stat_by_problem(self, problem)

    def is_problem_solved(self, problem):
        return self.stat.is_ok_problem(self, problem)

    def add_problem_result(self, tag, problem_result):
        self.problem_results[tag] = problem_result
        self.total_score += problem_result.score
        self.total_solved += problem_result.is_solved
