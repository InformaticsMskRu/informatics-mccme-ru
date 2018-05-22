from enum import Enum

from sqlalchemy import ForeignKey, Column, Unicode
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer

from pynformatics import EjudgeProblem
from pynformatics.model.meta import Base
from pynformatics.models import DBSession


class ProblemRequestStatus(Enum):
    REVIEW = 'review'
    APPROVED = 'approved'
    DECLINED = 'declined'


class ProblemRequest(Base):
    __tablename__ = 'mdl_problem_requests'
    __table_args__ = {'schema': 'pynformatics'}
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    name = Column(Unicode)
    content = Column(Unicode)
    status = Column(Unicode)

    user = relationship('User', lazy='joined')

    def __init__(self, problem_id, user_id, name, content,
                 status=ProblemRequestStatus.REVIEW.value):
        self.problem_id = problem_id
        self.user_id = user_id
        self.name = name
        self.content = content
        self.status = status

    def serialize(self, context) -> dict:
        attrs = [
            'id',
            'name',
            'content',
            'status',
        ]
        problem_dict = {
            attr: getattr(self, attr, 'undefined')
            for attr in attrs
        }
        problem = self.get_problem()
        if problem:
            problem_dict['problem'] = problem.serialize(context)

        if self.user:
            problem_dict['user'] = self.user.serialize(context)
        return problem_dict

    def get_problem(self) -> EjudgeProblem:
        return DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == self.problem_id).first()
