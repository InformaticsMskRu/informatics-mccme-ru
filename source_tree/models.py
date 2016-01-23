from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from pynformatics.model.meta import Base

DBSession = sessionmaker()
# db_session = DBSession()

# Base = declarative_base()

# from pynformatics.model.problem import Problem
from source_tree.model.problem import Problem
from pynformatics.model.statement import Statement, StatementProblem
from pynformatics.model.user import SimpleUser, User
from source_tree.model.source import Source
from source_tree.model.course import Course, CourseRaw, CourseTreeCap
from source_tree.model.role import Role, Context, RoleAssignment
