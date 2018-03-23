__all__ = ['Base', 'DBSession']

from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

from pynformatics.model.user import User, SimpleUser
from pynformatics.model.ejudge_run import EjudgeRun
from pynformatics.model.statement import Statement
from pynformatics.model.problem import Problem, EjudgeProblem
from pynformatics.model.comment import Comment
from pynformatics.model.stars import Stars
from pynformatics.model.ejudgeContest import EjudgeContest
