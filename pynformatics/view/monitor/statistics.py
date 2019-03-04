class Statistics:
    def sum(self, competitor):
        """
        :param competitor: участник
        :return: сумма по статистике.
        """
        raise NotImplementedError

    def get_stat_by_problem(self, competitor, problem):
        """
        :param competitor: участник.
        :param problem: таг задачи.
        :return: текстовое представление статистики для HTML результата задачи.
        """
        raise NotImplementedError

    def is_ok_problem(self, competitor, problem):
        try:
            return competitor.problem_results[hash(problem)].is_ok
        except KeyError:
            return False


class Score(Statistics):
    def sum(self, competitor):
        return competitor.total_score

    def get_stat_by_problem(self, competitor, problem):
        try:
            return competitor.problem_results[hash(problem)].str_score
        except KeyError:
            return ''


class Solved(Statistics):
    def sum(self, competitor):
        return competitor.total_solved

    def get_stat_by_problem(self, competitor, problem):
        try:
            return competitor.problem_results[hash(problem)].str_tries
        except KeyError:
            return ''
