"""The application's model objects"""
from pynformatics.model.meta import Session, Base
from pynformatics.model.user import User, SimpleUser, PynformaticsUser
from pynformatics.model.run import Run
from pynformatics.model.problem import Problem, EjudgeProblem, EjudgeProblemDummy
from pynformatics.model.statement import Statement
from pynformatics.model.comment import Comment
from pynformatics.model.stars import Stars
from pynformatics.model.ejudgeContest import EjudgeContest
from pynformatics.model.ideal_solution import Ideal
from pynformatics.model.group import Group, UserGroup
from pynformatics.model.hint import Hint
from pynformatics.model.recommendation import Recommendation
from pynformatics.model.contests_statistic import ContestsStatistic

__all__ = [
    'action',
    'comment',
    'contests_statistic',
    'course',
    'course_module',
    'ejudgeContest',
    'group',
    'group_invite',
    'hint',
    'ideal_solution',
    'log',
    'meta',
    'participant',
    'problem',
    'pynformatics_run',
    'recommendation',
    'run',
    'standings',
    'stars',
    'statement',
    'user',
    'user_oauth_provider'
]


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
