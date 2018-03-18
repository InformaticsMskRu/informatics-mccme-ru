from sqlalchemy import (
    Column,
    ForeignKey,
    ForeignKeyConstraint,
    UniqueConstraint,
)
from sqlalchemy.types import Integer, String, Text, Float, Unicode
from sqlalchemy.orm import relationship, backref, relation

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from pynformatics.model.meta import Base
from pynformatics.models import DBSession
from pynformatics.utils.functions import attrs_to_dict


class  Group(Base):
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

    def serialize(self, context, attributes=None):
        if not attributes:
            attributes = (
                'name',
                'description',
                'owner_id',
                'visible',
            )
        serialized = attrs_to_dict(self, *attributes)
        return serialized


class UserGroup(Base):
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id', name='group_id'),
        {'schema':'moodle'},
    )
    __tablename__ = 'mdl_ejudge_group_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    group_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_group.id'))

    user = relationship('SimpleUser', backref=backref('user_groups', lazy='select'))
    group = relationship('Group', backref=backref('user_groups', lazy='select'))

    @staticmethod
    def create_if_not_exists(user_id, group_id):
        user_group = DBSession.query(UserGroup).filter_by(
            user_id=user_id,
            group_id=group_id
        ).first()
        if user_group:
            return None

        return UserGroup(user_id=user_id, group_id=group_id)
