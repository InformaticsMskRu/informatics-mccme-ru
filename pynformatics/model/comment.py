"""Run model"""

from sqlalchemy.sql.expression import and_
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.schema import ForeignKeyConstraint
from pynformatics.model.meta import Base
from pynformatics.model import EjudgeRun, User, SimpleUser
import datetime

class Comment(Base):
    __tablename__ = "mdl_run_comments"
    __table_args__ = (
        ForeignKeyConstraint(['run_id', 'contest_id'], ['ejudge.runs.run_id', 'ejudge.runs.contest_id']),
        {'schema':'ejudge'}
    )
   
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    run_id = Column(Integer)
    contest_id = Column(Integer)
    user_id = Column(Integer)
    author_user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    author_user = relationship(SimpleUser, backref = backref('simpleuser1'), uselist=False, lazy=False, primaryjoin = author_user_id == SimpleUser.id)
    run = relationship('EjudgeRun', backref = backref('run'), uselist=False)
    lines = Column(Text)
    comment = Column(Unicode)
    is_read = Column(Boolean)
    def __init__(self,  run, author, lines = '', comment = '', date = datetime.datetime.now()):
        self.date = date
        self.run_id = run.run_id
        self.user_id = run.user.id
        self.contest_id = run.contest_id
        self.author_user_id = author.id
        self.lines = lines    
        self.comment = comment    
        self.is_read = False
        

    def __json__(self, request):
        return {
            'date' : str(self.date),
            'id' :  self.id,
            'run_id' : self.run_id,
            'user_id' : self.user_id,
            'contest_id' : self.contest_id,
            'author_user_id' : self.author_user_id,
            'lines' : self.lines,
            'comment' : self.comment,
            'is_read' : self.is_read,
            'problem_id' : self.run.problem.id,
            'problem_name' : self.run.problem.name
        }
    

    def get_by(run_id, contest_id):
        try:
            return Session.query(Comment).filter(Comment.run.run_id == int(run_id)).filter(Comment.contest_id == int(contest_id)).first()            
        except:
            return None
    get_by = staticmethod(get_by)        