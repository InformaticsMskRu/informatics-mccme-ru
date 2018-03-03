"""Group model"""
from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    Boolean
)
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship, backref


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
    visible = Column(Integer)

    owner = relationship('SimpleUser', backref=backref('groups', lazy='select'), lazy='joined')

    def serialize(self, context=None, attributes=None):
        if not attributes:
            attributes = (
                'id',
                'name',
                'description',
                'owner_id',
                'visible',
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

class GroupInviteLinkWithContest(Base):
    __tablename__ = "group_invite_link_with_statement"
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("moodle.mdl_ejudge_group.id"))
    contest_id = Column(Integer, ForeignKey("moodle.mdl_ejudge_contest.id"))
    is_active = Column(Boolean)

    def __init__(self, group_id, contest_id):
        self.group_id = group_id
        self.contest_id = contest_id
        self.is_active = True

    def serialize(self, context=None, attributes=('id', 'group_id', 'contest_id', 'is_active')):
        return {
            'link': IntUrlGenerator().encode(self.id),
            **attrs_to_dict(self, *attributes)
        }
