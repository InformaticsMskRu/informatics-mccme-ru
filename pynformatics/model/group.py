"""Group model"""
from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Boolean
)
from sqlalchemy.types import Integer, Unicode, Enum
from sqlalchemy.orm import relationship, backref

from pynformatics.model import Statement, EjudgeContest
from pynformatics.model.course import Course
from pynformatics.model.meta import Base
from pynformatics.utils.functions import attrs_to_dict
from pynformatics.utils.url_generator import IntUrlGenerator


class Group(Base):
    __tablename__ = 'mdl_ejudge_group'
    __table_args__ = (
        ForeignKeyConstraint(
            ['owner_id'],
            ['moodle.mdl_user.id']
        ),
        {'schema': 'moodle'}
    )

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    owner_id = Column(Integer)
    visible = Column(Boolean, default=True)

    owner = relationship('SimpleUser', backref=backref('groups', lazy='select'), lazy='joined')

    def serialize(self, context=None, attributes=None):
        if not attributes:
            attributes = (
                'id',
                'name',
                'description',
                'owner_id',
                'visible'
            )
        serialized = attrs_to_dict(self, *attributes)
        return serialized


class UserGroup(Base):
    __tablename__ = 'mdl_ejudge_group_users'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    group_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_group.id'))

    group = relationship('Group', backref=backref('user_groups', lazy='select'))
    user = relationship('SimpleUser', backref=backref('user_groups', lazy='select'))


class GroupInviteLink(Base):
    __tablename__ = "group_invite_link"
    __table_args__ = {'schema': 'moodle'}

    REDIRECT_TYPES = ('STATEMENT', 'CONTEST', 'COURSE')

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("moodle.mdl_ejudge_group.id"))
    redirect_type = Column(Enum(*REDIRECT_TYPES))
    redirect_id = Column(Integer)
    is_active = Column(Boolean)

    def __init__(self, group_id, redirect_type=None, redirect_id=None):
        self.group_id = group_id
        self.redirect_type = redirect_type
        self.redirect_id = redirect_id
        self.is_active = True

    def get_redirect(self, session):
        if self.redirect_type is None or self.redirect_id is None:
            return None
        redirect_classes = {
            'STATEMENT': Statement,
            'CONTEST': EjudgeContest,
            'COURSE': Course
        }
        return session.query(redirect_classes[self.redirect_type])\
            .filter(redirect_classes[self.redirect_type].id==self.redirect_id).one()

    def get_link(self):
        return IntUrlGenerator().encode(self.id)

    def serialize(self, context=None,
                  attributes=('id', 'group_id', 'redirect_type', 'redirect_id', 'is_active')):
        return {
            'link': self.get_link(),
            **attrs_to_dict(self, *attributes)
        }
