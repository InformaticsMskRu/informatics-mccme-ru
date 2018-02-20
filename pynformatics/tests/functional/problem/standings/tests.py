import datetime
from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.model.run import Run
from pynformatics.testutils import TestCase


class TestApi__problem_standings(TestCase):
    def setUp(self):
        super(TestApi__problem_standings, self).setUp()

        self.create_problems()
        self.create_users()

    def send_request(self,
                     problem_id=1,
                     status=200,
                     ):
        response = self.app.get(
            url='/problem/%s/standings' % problem_id,
            status=status
        )
        return response

    def test_maximum(self):
        """
        В таблице будет показан максимум по задаче, а не результат последней посылки.
        Количество попыток равно количеству посылок
        """
        scores = [20, 70, 40]
        statuses = [7, 12, 7]
        runs = [
            Run(
                run_id=index,
                score=score,
                status=status,
                user_id=self.users[0].ejudge_id,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
            )
            for index, score, status in zip(range(3), scores, statuses)
        ]
        self.session.add_all(runs)

        response = self.send_request()
        assert_that(
            response.json,
            equal_to({
                '1': {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 3,
                    'score': 70,
                    'status': 12,
                }
            })
        )

    def test_ignores_after_ok(self):
        """
        Игнорирует все посылки после первого ОК за задачу.
        Количество попыток 2, хотя посылок 3
        """
        scores = [20, 100, 40]
        statuses = [7, 0, 7]
        runs = [
            Run(
                run_id=index,
                score=score,
                status=status,
                user_id=self.users[0].ejudge_id,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
            )
            for index, score, status in zip(range(3), scores, statuses)
        ]
        self.session.add_all(runs)

        response = self.send_request()
        assert_that(
            response.json,
            equal_to({
                '1': {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 2,
                    'score': 100,
                    'status': 0,
                }
            })
        )

    def test_sorts_by_time(self):
        """
        Есть две посылки на максимальное число баллов.
        Оценивается та, что послана раньше (create_time у третьей меньше, чем у второй)
        """
        scores = [20, 40, 40]
        statuses = [7, 12, 7]
        create_times = [
            datetime.datetime(2018, 2, 22, 17, 30, 0),
            datetime.datetime(2018, 2, 22, 17, 40, 0),
            datetime.datetime(2018, 2, 22, 17, 35, 0),
        ]
        runs = [
            Run(
                run_id=index,
                score=score,
                status=status,
                create_time=create_time,
                user_id=self.users[0].ejudge_id,
                contest_id=self.problems[0].ejudge_contest_id,
                prob_id=self.problems[0].problem_id,
            )
            for index, score, status, create_time in zip(
                range(3),
                scores,
                statuses,
                create_times
            )
        ]
        self.session.add_all(runs)

        response = self.send_request()
        assert_that(
            response.json,
            equal_to({
                '1': {
                    'firstname': 'Maxim',
                    'lastname': 'Grishkin',
                    'attempts': 3,
                    'score': 40,
                    'status': 7,
                }
            })
        )

    def test_not_found(self):
        response = self.send_request(problem_id=123, status=404)
        assert_that(
            response.json,
            equal_to({
                'code': 404,
                'message': 'No problem with this id'
            })
        )

    def test_does_not_create_twice(self):
        # Ошибку будет кидать база при попытке создать объект с не уникальним ключом
        self.send_request()
        self.send_request()
