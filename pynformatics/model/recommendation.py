"""Recommendation model"""
from sqlalchemy.sql.expression import and_
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.schema import ForeignKeyConstraint
from pynformatics.model.meta import Base
from pynformatics.model import User
from pynformatics.models import DBSession


class Recommendation(Base):
    __tablename__ = "sis_most_popular_next_problems_recommendations"
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer)
    contest_id = Column(Integer)

    recommended_problem_id = Column(Integer)
    recommended_contest_id = Column(Integer)

    def __init__(self, contest_id, problem_id, recommended_contest_id, recommended_problem_id):
        self.contest_id = contest_id
        self.problem_id = problem_id
        self.recommended_contest_id = recommended_contest_id
        self.recommended_problem_id = recommended_problem_id

    def get_by(self, contest_id, problem_id):
        try:
            return DBSession.query(Recommendation).filter(Recommendation.contest_id == int(contest_id)).filter(Recommendation.problem_id == int(problem_id))
        except:
            return None

    def __json__(self, request):
        return {
            'id' :  self.id,
            'problem_id' : self.problem_id,
            'contest_id': self.contest_id,
            'recommended_contest_id' : self.lang_id,
            'recommended_problem_id' : self.test_signature,
        }

