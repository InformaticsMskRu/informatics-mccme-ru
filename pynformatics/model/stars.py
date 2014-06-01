"""Run model"""

from sqlalchemy.sql.expression import and_
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Text, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.schema import ForeignKeyConstraint
from pynformatics.model.meta import Base
from pynformatics.model import User, SimpleUser
import datetime


class Stars(Base):
    __tablename__ = "mdl_stars"
    __table_args__ = {'schema': 'moodle'}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    # user = relationship(SimpleUser, backref = backref('simpleuser1'), uselist=False, lazy=False, primaryjoin = user_id == SimpleUser.id)
    title = Column(Unicode)
    link = Column(Unicode)

    def __init__(self, user, title, link):
        self.link = link
        self.title = title
        self.user_id = user.id

    def __json__(self, request):
        return {
            'id' :  self.id,
            'user_id' : self.user_id,
            'title' : self.title,
            'link' : self.link,
        }
