import string
from enum import Enum


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

    def __init__(self, problem_meta, number, contest, seen_problems):
        self.id = problem_meta['id']
        self.name = problem_meta['name']
        self.rank = problem_meta['rank']
        self.number = number
        self.contest_id = contest.id
        self.contest_rank = contest.rank
        self.was_seen = self.id in seen_problems

    def __hash__(self):
        return hash((self.id, self.contest_id))

    @property
    def full_tag(self):
        """
        :return: таг задачи в формате {номер контеста}{буквенный номер задачи}
        """
        return '{}{}'.format(self.contest_rank, self.RANK_TO_LETTER[self.number])

    @property
    def tag(self):
        """
        :return: таг задачи в формате {номер контеста}{буквенный номер задачи}
        """
        return str(self.RANK_TO_LETTER[self.number])


# TODO: Добавить в репозиторий Enum со статусами, а не просто писать Magic number`ы
class ProblemResultColor(Enum):
    WHITE = ({99, 14, 1, 10, 7, 11, 2, 3, 4, 5, 6, 12, 13}, '#fff')
    GREEN = ({0}, '#e1f2e1')
    YELLOW = ({8}, ' #ffff66')
    RED = ({9}, '#ff6666')

    def __init__(self, statuses, html_color):
        self.statuses = statuses
        self.html_color = html_color

    @classmethod
    def get_by_status(cls, status):
        def eq(color):
            return status in color.statuses

        try:
            return next(filter(eq, cls))
        except StopIteration:
            raise ValueError('Such status does not exist')
# TODO: Вывести более дружелюбное сообщение с перечислением возможных статусов.
#  Но для этого нужно сделать to do выше :) и добавить метод по типу __str__ в enum.


class ProblemResult:
    MAX_SCORE = 100

    def __init__(self, run_scores, run_statuses, seen):
        """
        Создать результат по задаче.
        Выбирается посылка с наибольшим баллом и количество посылок.
        :param run_scores: все посылки.
        """
        self.score = max(run_scores)
        self.tries = len(run_scores)
        last_status = run_statuses[-1]
        self.color = ProblemResultColor.get_by_status(last_status)
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
