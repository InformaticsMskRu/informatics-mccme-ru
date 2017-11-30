from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode, Boolean
from sqlalchemy.orm import relationship, backref

from pynformatics.model.meta import Base


class UserOAuthProvider(Base):
    __table_args__ = {'schema': 'pynformatics'}
    __tablename__ = 'user_oauth_provider'

    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'), primary_key=True)
    provider = Column(String, primary_key=True)
    oauth_id = Column(String)

    user = relationship('User', backref=backref('oauth_ids', lazy='select'))
