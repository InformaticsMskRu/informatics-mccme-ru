"""Run model"""

from sqlalchemy.sql.expression import and_
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.schema import ForeignKeyConstraint
from pynformatics.model.meta import Base
from pynformatics.model import Run, User
from pynformatics.models import DBSession


class Hint(Base):
    __tablename__ = "sis_hint"
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    contest_id = Column(Integer, ForeignKey('ejudge.runs.contest_id'))
    lang_id = Column(Integer)
    test_signature = Column(Unicode)
    comment = Column(Unicode)

    def __init__(self, problem_id, contest_id, lang_id, test_signature, comment):
        self.problem_id = problem_id
        self.contest_id = contest_id
        self.lang_id = lang_id
        self.test_signature = test_signature
        self.comment = comment
        
    def get_by(contest_id, problem_id, lang_id, signature):
        try:  # lang_id is ignored, cause we don't have hints for each language
            return DBSession.query(Hint).filter(Hint.contest_id == int(contest_id)).filter(Hint.problem_id == int(problem_id)).filter(Hint.test_signature == signature).first()            
        except:
            return None

    def __json__(self, request):
        return {
            'id' :  self.id,
            'problem_id' : self.problem_id,
            'contest_id': self.contest_id,
            'lang_id' : self.lang_id,
            'test_signature' : self.test_signature,
            'comment': self.comment,
        }
