from collections import namedtuple
from itertools import groupby
from operator import itemgetter, attrgetter

from pynformatics.view.monitor.competitor import Competitor
from pynformatics.view.monitor.problem import ProblemResult, Problem
from pynformatics.view.monitor.statistics import Solved, Score

# TODO: пока нет name в json, вставляю тоже con_id
Contest = namedtuple('Contest', 'id rank name')


class MonitorRenderer:
    STATS = {'partial_scores_on': Score(), 'partial_scores_off': Solved()}
    NON_TERMINAL = {96, 98}

    def __init__(self, data, stat='score'):
        if stat not in self.STATS:
            msg = 'Invalid value for stat parameter: {0}, possible parameters: {1}.'
            raise ValueError(msg.format(stat, ', '.join(self.STATS.keys())))
        self.stat = self.STATS[stat]
        self.problems = data

    def render(self):
        contests = []
        problems = []
        seen_problems = set()
        competitors = {}

        for con_rank, (con_id, c_problems) in enumerate(
            groupby(self.problems, key=itemgetter('contest_id')), start=1
        ):
            contest = Contest(con_id, con_rank, con_id)
            contests.append(contest)
            for c_problem in sorted(c_problems, key=lambda x: x['problem']['rank']):
                problem_meta = c_problem['problem']
                p = Problem(problem_meta, contest, seen_problems)
                problems.append(p)
                runs = c_problem['runs']
                self._process_runs(p, runs, competitors)
                seen_problems.add(p.id)

        competitors = self._process_competitors(competitors)
        contests_table = self._process_contests(contests, problems)
        return problems, competitors, contests_table

    def _process_runs(self, problem, runs, comps):
        def get_user_id(run):
            return run['user']['id']

        runs.sort(key=get_user_id)
        comp_ids = []
        group_runs = []
        for comp_id, comp_runs in groupby(runs, key=get_user_id):
            comp_ids.append(comp_id)
            group_runs.append(list(comp_runs))

        for comp_id, comp_runs in zip(comp_ids, group_runs):
            if comp_id not in comps:
                f_name = comp_runs[0]['user']['firstname']
                l_name = comp_runs[0]['user']['lastname']
                comps[comp_id] = Competitor(comp_id, f_name, l_name)

            comp_runs = filter(self._is_correct_run, comp_runs)

            runs_scores = []
            runs_statuses = set()
            for run in comp_runs:
                runs_scores.append(run['ejudge_score'])
                runs_statuses.add(run['ejudge_status'])

            if runs_scores:
                print(runs_statuses)
                assert runs_statuses
                comps[comp_id].add_problem_result(
                    hash(problem),
                    ProblemResult(runs_scores, runs_statuses, problem.was_seen),
                )

    def _is_correct_run(self, run):
        """
        Корректная ли посылка.
        1. Не None
        2. Не промежуточный статус (не тестирование, не компилирование).
        :param run: Посылка.
        """
        return (
            run['ejudge_score'] is not None
            and run['ejudge_status'] not in self.NON_TERMINAL
        )

    def _process_competitors(self, competitors):
        competitors = list(competitors.values())
        for c in competitors:
            c.stat = self.stat
        competitors.sort(key=lambda x: x.sum(), reverse=True)
        return competitors

    @staticmethod
    def _process_contests(contests, problems):
        contests_table = [['Letter', 'Name']]
        keyfunc = attrgetter('contest_id')
        problems_by_contest = (g for _, g in groupby(problems, key=keyfunc))
        for contest, problem_g in zip(contests, problems_by_contest):
            contests_table.append(['Contest', contest.id])
            for problem in problem_g:
                contests_table.append(
                    [problem.tag, '{0} [{1}]'.format(problem.name, problem.id)]
                )
        return contests_table
