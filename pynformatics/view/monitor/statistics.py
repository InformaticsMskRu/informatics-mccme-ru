class Statistics:
    def sum(self, competitor):
        """
        :param competitor: участник
        :return: сумма по статистике.
        """
        raise NotImplementedError

    def get_stat_by_problem(self, competitor, problem_tag):
        """
        :param competitor: участник.
        :param problem_tag: таг задачи.
        :return: текстовое представление статистики для HTML результата задачи.
        """
        raise NotImplementedError

    def is_problem_solved(self, competitor, problem_tag: str):
        try:
            return competitor.problem_results[problem_tag].is_solved
        except KeyError:
            return False


class Score(Statistics):
    def sum(self, competitor):
        return competitor.total_score

    def get_stat_by_problem(self, competitor, problem_tag: str):
        try:
            return competitor.problem_results[problem_tag].str_score
        except KeyError:
            return ''


class Solved(Statistics):
    def sum(self, competitor):
        return competitor.total_solved

    def get_stat_by_problem(self, competitor, problem_tag: str):
        try:
            return competitor.problem_results[problem_tag].str_tries
        except KeyError:
            return ''
