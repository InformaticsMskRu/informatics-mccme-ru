from sqlalchemy import (
    Column,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import Integer

from pynformatics.model.meta import Base


class CourseModule(Base):
    __table_args__ = {'schema': 'moodle'}
    __tablename__ = 'mdl_course_modules'

    id = Column(Integer, primary_key=True)
    course_id = Column('course', Integer, ForeignKey('moodle.mdl_course.id'))
    instance = Column(Integer)
    module = Column(Integer)

    course = relationship('Course', backref='course_module')
