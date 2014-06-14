"""The application's model objects"""
from pynformatics.model.meta import Session, Base
from pynformatics.model.user import User, SimpleUser, PynformaticsUser, EjudgeUser
from pynformatics.model.run import Run
from pynformatics.model.problem import Problem, EjudgeProblem
from pynformatics.model.statement import Statement
from pynformatics.model.comment import Comment
from pynformatics.model.stars import Stars
from pynformatics.model.ejudgeContest import EjudgeContest
from pynformatics.model.ideal_solution import Ideal

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
