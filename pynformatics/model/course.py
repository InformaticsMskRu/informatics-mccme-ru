from sqlalchemy import Column
from sqlalchemy.types import (
    Boolean,
    Integer,
    Unicode,
)

from pynformatics.model.meta import Base
from pynformatics.utils.functions import attrs_to_dict


class Course(Base):
    __table_args__ = {'schema': 'moodle'}
    __tablename__ = 'mdl_course'

    id = Column(Integer, primary_key=True)

    full_name = Column('fullname', Unicode)
    short_name = Column('shortname', Unicode)

    category = Column(Integer)
    password = Column(Unicode)
    visible = Column(Boolean)

    def require_password(self):
        return bool(self.password)

    def serialize(self, context):
        serialized = attrs_to_dict(
            self,
            'id',
            'full_name',
            'short_name',
        )
        serialized['require_password'] = self.require_password()
        return serialized
