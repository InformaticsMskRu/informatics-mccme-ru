import string
from enum import Enum
from operator import itemgetter


class Problem:
    """
    Задача в контексте соревнования(контеста).

    Задачи в таблице могут повторяться так как в сводной таблице могут
    быть несколько соревнований за разное время с повторяющимся задачами.
    Это означает что у одинаковых задач будут одинаковые идентификаторы, но разные таги.
    """

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
        return '{}{}'.format(self.contest_rank, self.number_to_tag(self.number))

    @property
    def tag(self):
        """
        :return: таг задачи в формате {буквенный номер задачи}
        """
        return self.number_to_tag(self.number)

    def number_to_tag(self, number):
        """1 -> A, ..., 26 -> Z, 27 -> AA"""
        result = []
        while number:
            result.append(string.ascii_uppercase[(number - 1) % 26])
            number = (number - 1) // 26
        return ''.join(reversed(result))


# TODO: Добавить в репозиторий Enum со статусами, а не просто писать Magic number`ы
class Status(Enum):
    EJUDGE_OK = ({0}, '#e1f2e1')
    JUDGE_OK = ({8}, ' #ffff66')
    # TODO: Выяснить являются ли wrong статусами:
    #  1 - Ошибка компиляции
    #  12 - Превышение лимита памяти
    #  13 - Security error
    #  14 - Ошибка оформления кода
    WRONG = ({2, 3, 4, 5, 6, 7}, '#fff')
    JUDGE_WRONG = ({9}, '#ff6666')
    # Статусы, которые никак не влияют на подсчеты, но должны быть белого цвета
    OTHER = ({}, '#fff')

    def __init__(self, codes, html_color):
        self.codes = codes
        self.html_color = html_color

    @classmethod
    def by_code(cls, code):
        def eq(status):
            return code in status.codes

        try:
            return next(filter(eq, cls))
        except StopIteration:
            return cls.OTHER


# TODO: Вывести более дружелюбное сообщение с перечислением возможных статусов.
#  Но для этого нужно сделать to do выше :) и добавить метод по типу __str__ в enum.


class ProblemResult:
    def __init__(self, runs, seen):
        """
        Создать результат по задаче.
        Выбирается посылка с наибольшим баллом и количество посылок.
        :param runs: все посылки.
        """
        self.score = max(map(itemgetter('ejudge_score'), runs))
        codes = map(itemgetter('ejudge_status'), runs)
        self.tries = sum(Status.by_code(code) is Status.WRONG for code in codes)
        last_status = runs[-1]['ejudge_status']
        self.status = Status.by_code(last_status)
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
        if not self.tries:
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
        return self.status is Status.JUDGE_OK or self.status is Status.EJUDGE_OK
