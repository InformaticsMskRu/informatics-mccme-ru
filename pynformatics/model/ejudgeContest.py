"""Problem model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import *
from sqlalchemy.orm import relationship, backref, relation
import datetime 
from pynformatics.view.utils import *

from pynformatics.model.meta import Base

class EjudgeContest(Base):
    __tablename__ = "mdl_ejudge_contest"
    __table_args__ = {'schema':'moodle'}
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    ejudge_id = Column(Text)
    ejudge_int_id = Column(Integer, nullable=False, primary_key=True, autoincrement=False)
    load_time = Column(DateTime)
    
    def __init__(self, name='', ejudge_int_id = 0):
        self.name = name
        self.ejudge_id = getContestStrId(ejudge_int_id)
        self.ejudge_int_id = ejudge_int_id
        self.load_time = datetime.datetime.now()
        