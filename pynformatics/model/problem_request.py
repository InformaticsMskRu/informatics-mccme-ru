from enum import Enum

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Unicode

from pynformatics import EjudgeProblem, User
from pynformatics.model.meta import Base
from pynformatics.models import DBSession


class ProblemRequestStatus(Enum):
    REVIEW = 'review'
    APPROVED = 'approved'
    DECLINED = 'declined'

    @staticmethod
    def from_str(value):
        if value == ProblemRequestStatus.REVIEW.value:
            return ProblemRequestStatus.REVIEW
        elif value == ProblemRequestStatus.APPROVED.value:
            return ProblemRequestStatus.APPROVED
        elif value == ProblemRequestStatus.DECLINED.value:
            return ProblemRequestStatus.DECLINED
        return None


class ProblemRequest(Base):
    __tablename__ = 'mdl_problem_requests'
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    problem_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_problem.id'))
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    name = Column(Unicode)
    content = Column(Unicode)
    status = Column(Unicode)

    def __init__(self, problem_id, user_id, name, content, status=ProblemRequestStatus.REVIEW.value):
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
        user = self.get_user()
        if user:
            problem_dict['user'] = user.serialize(context)
        return problem_dict

    def get_problem(self) -> EjudgeProblem:
        return DBSession.query(EjudgeProblem).filter(EjudgeProblem.id == self.problem_id).first()

    def get_user(self) -> User:
        return DBSession.query(User).filter(User.id == self.user_id).first()
