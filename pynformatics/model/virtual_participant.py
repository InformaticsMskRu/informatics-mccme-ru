import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy.types import Integer, String, Text, Float, Unicode

from pynformatics.model.meta import Base
from pynformatics.utils.functions import attrs_to_dict


class VirtualParticipant(Base):
    __table_args__ = {'schema': 'moodle'}
    __tablename__ = 'mdl_virtualcontest'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    statement_id = Column(Integer, ForeignKey('moodle.mdl_statements.id'))
    start = Column(Integer)
    duration = Column(Integer)

    statement = relationship('Statement', backref=backref('virtual_participants', lazy='dynamic'))

    def finished(self):
        finish_time = datetime.datetime.fromtimestamp(self.start) + datetime.timedelta(minutes=self.duration)
        return datetime.datetime.now() >= finish_time

    def serialize(self, context):
        return attrs_to_dict(
            self,
            'start',
            'duration',
            'statement_id',
        )
