from pynformatics.view.monitor.problem import Status


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

    def problem_status(self, competitor, problem):
        try:
            return competitor.problem_results[problem].status
        except KeyError:
            return Status.OTHER


class Score(Statistics):
    def sum(self, competitor):
        return competitor.total_score

    def get_stat_by_problem(self, competitor, problem):
        try:
            return competitor.problem_results[problem].str_score
        except KeyError:
            return ''


class Solved(Statistics):
    def sum(self, competitor):
        return competitor.total_solved

    def get_stat_by_problem(self, competitor, problem):
        try:
            return competitor.problem_results[problem].str_tries
        except KeyError:
            return ''
