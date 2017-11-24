from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Text, Float, Unicode

from pynformatics.model.meta import Base


class CourseModule(Base):
    __table_args__ = {'schema': 'moodle'}
    __tablename__ = 'mdl_course_modules'

    id = Column(Integer, primary_key=True)
    course = Column(Integer)
    instance = Column(Integer)
    module = Column(Integer)
