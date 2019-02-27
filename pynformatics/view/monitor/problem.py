import string


class Problem:
    """
    Задача в контексте соревнования(контеста). Задачи в таблице могут повторяться
    так как в сводной таблице могут быть несколько соревнований
    за разное время с повторяющимся задачами.

    Это означает что у одинаковых задач будут одинаковые идентификаторы,
    но разные таги.
    """

    # 1 -> A, ..., 26 -> Z
    RANK_TO_LETTER = dict(enumerate(string.ascii_uppercase, start=1))

    def __init__(self, problem_meta, contest, seen_problems):
        self.id = problem_meta['id']
        self.name = problem_meta['name']
        self.rank = problem_meta['rank']
        self.contest_id = contest.id
        self.contest_rank = contest.rank
        self.was_seen = self.id in seen_problems

    def __hash__(self):
        return hash((self.id, self.contest_id))

    @property
    def tag(self):
        """
        :return: таг задачи в формате {номер контеста}{буквенный номер задачи}
        """
        return '{}{}'.format(self.contest_rank, self.RANK_TO_LETTER[self.rank])


class ProblemResult:
    MAX_SCORE = 100

    def __init__(self, runs, seen):
        """
        Создать результат по задаче.
        Выбирается посылка с наибольшим баллом и количество посылок.
        :param runs: все посылки.
        """
        self.score = max(runs)
        self.tries = len(runs)
        self.was_seen = seen

    @property
    def str_score(self):
        """
        :return: текстовое представление результата задачи для HTML.
        """
        if self.score:
            if self.was_seen:
                return '({})'.format(self.score)
            return str(self.score)
        return ''

    @property
    def str_tries(self):
        """
        :return: текстовое представление количества попыток решения задачи для HTML.
        """
        if self.score == 0:
            return ''
        if self.is_solved:
            res = '+{}'.format(self.tries - 1 or '')
        else:
            res = '-{}'.format(self.tries)
        if self.was_seen:
            return '({})'.format(res)
        return res

    @property
    def is_solved(self):
        """
        :return: решена ли задача на максимальный балл.
        """
        return self.score == self.MAX_SCORE
