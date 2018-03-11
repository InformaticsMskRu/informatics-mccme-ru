from sqlalchemy import (
    Column,
    ForeignKey
)
from sqlalchemy.orm import (
    backref,
    relationship,
)
from sqlalchemy.sql import func
from sqlalchemy.types import (
    DateTime,
    Integer,
    String,
    Text,
)

from pynformatics.model.action import Action
from pynformatics.model.meta import Base
from pynformatics.model.user import SimpleUser


class Log(Base):
    """
    Модель лога действия пользователя.
    """
    __table_args__ = {'schema': 'pynformatics'}
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    instance_id = Column(Integer)
    action_id = Column(Integer, ForeignKey('pynformatics.action.id'))

    created_at = Column(DateTime, default=func.now())

    action = relationship('Action', backref=(backref('logs', lazy='select')), lazy='joined')
    user = relationship('SimpleUser', backref=backref('logs', lazy='select'), lazy='joined')
