from collections import namedtuple
from itertools import groupby
from operator import itemgetter, attrgetter

from pynformatics.view.monitor.competitor import Competitor
from pynformatics.view.monitor.problem import ProblemResult, Problem
from pynformatics.view.monitor.statistics import Solved, Score

# TODO: пока нет name в json, вставляю тоже con_id
Contest = namedtuple('Contest', 'id rank name')


class MonitorRenderer:
    STATS = {'partial_score': Score(), 'partial_score_off': Solved()}

    def __init__(self, data, stat='score'):
        if stat in self.STATS:
            self.stat = self.STATS[stat]
        else:
            msg = 'Invalid value for stat parameter: {0}, possible parameters: {1}.'
            raise ValueError(msg.format(stat, ', '.join(self.STATS.keys())))
        self.problems = data['data']

    def render(self):
        contests = []
        problems = []
        seen_problems = set()
        competitors = {}

        keyfunc = itemgetter('contest_id')
        self.problems.sort(key=keyfunc)
        for con_rank, (con_id, c_problems) in enumerate(
            groupby(self.problems, key=keyfunc), start=1
        ):
            contest = Contest(con_id, con_rank, con_id)
            contests.append(contest)
            for c_problem in sorted(c_problems, key=lambda x: x['problem']['rank']):
                problem_meta = c_problem['problem']
                p = Problem(**problem_meta, contest=contest, seen=seen_problems)
                problems.append(p)
                runs = c_problem['runs']
                self._process_runs(p, runs, competitors)
                seen_problems.add(p.id)

        competitors = self._process_competitors(competitors)
        contests_table = self._process_contests(contests, problems)
        return problems, competitors, contests_table

    @staticmethod
    def _process_runs(problem, runs, comps):
        def get_user_id(run: dict):
            return run['user']['id']

        key = get_user_id
        runs.sort(key=key)

        comp_ids = []
        group_runs = []

        for comp_id, comp_data in groupby(runs, key=key):
            comp_ids.append(comp_id)
            group_runs.append(list(comp_data))

        for comp_id, comp_data in zip(comp_ids, group_runs):
            if comp_id not in comps:
                f_name = comp_data[0]['user']['firstname']
                l_name = comp_data[0]['user']['lastname']
                comps[comp_id] = Competitor(comp_id, f_name, l_name)

            raw_runs_scores = (d['ejudge_score'] for d in comp_data)
            runs_scores = list(filter(None, raw_runs_scores))
            if runs_scores:
                comps[comp_id].add_problem_result(
                    problem.name, ProblemResult(runs_scores, problem.was_seen)
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
