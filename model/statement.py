"""Problem model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Text, Float, Unicode
from sqlalchemy.orm import relationship, backref, relation

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from pynformatics.model.meta import Base

class Statement(Base):
    __tablename__ = "mdl_statements"
    __table_args__ = {'schema':'moodle'}
    id = Column(Integer, primary_key=True)
    course = Column(Integer)
    name = Column(Unicode)
    summary = Column(Unicode)
    numbering = Column(Integer)
    disableprinting = Column(Integer)
    customtitles = Column(Integer)
    timecreated = Column(Integer)
    timemodified = Column(Integer)
    contest_id = Column(Integer)
    timestart = Column(Integer)
    timestop = Column(Integer)
    olympiad = Column(Integer)
#    analysis = Column(Unicode)
#    pr_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
#    ejudge_users = relation('EjudgeUser', backref="moodle.mdl_user", uselist=False)
#    ejudge_user = relation('EjudgeUser', backref = backref('moodle.mdl_user'), uselist=False, primaryjoin = "EjudgeUser.user_id == User.id")
    
    problems = association_proxy("StatementProblems", 'problem')
    user = association_proxy("StatementUsers1", 'user')
    
    def __init__(self, name, timelimit, memorylimit, content='', review='', description='', analysis=''):
        self.name = name
        self.content = content
        self.review = review
        self.description = description
        self.analysis = analysis
        self.hidden = 1
        self.timelimit = timelimit
        self.memorylimit = memorylimit

class StatementUser(Base):
    __tablename__ = 'mdl_olympiad'
    __table_args__ = {'schema':'moodle'}

    id = Column(Integer, primary_key=True)    
    statement_id = Column('contest_id', Integer, ForeignKey('moodle.mdl_statements.id'))
    user_id = Column(Integer, ForeignKey('moodle.mdl_user_ejudge.id'))

#    statement = relationship("Statement", backref=backref("StatementUsers1", lazy="dynamic"), lazy="dynamic")
#    user = relationship("EjudgeUser", backref=backref("StatementUsers2", lazy="dynamic"), lazy="dynamic")             
        
class StatementProblem(Base):
    __tablename__ = 'mdl_statements_problems_correlation'
    __table_args__ = {'schema':'moodle'}

    id = Column(Integer, primary_key=True)    
    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'))
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    rank = Column('rank', Integer)
    hidden = Column('hidden', Integer)

    statement = relationship("Statement", backref=backref("StatementProblems", collection_class=attribute_mapped_collection("rank")))

    # reference to the "Keyword" object
    problem = relationship("Problem", backref=backref("StatementProblems"))        
    
    def __init__(self, statement_id, problem_id, rank):
        self.statement_id = statement_id
        self.problem_id = problem_id
        self.rank = rank
        self.hidden = 0
