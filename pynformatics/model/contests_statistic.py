from sqlalchemy import Column
from sqlalchemy.types import Integer

from pynformatics.model.meta import Base

class ContestsStatistic(Base):
    __tablename__ = "contests_statistic"
    __table_args__ = {'schema':'moodle'}
    contest_id = Column(Integer, primary_key=True)
    submits_count = Column(Integer)
