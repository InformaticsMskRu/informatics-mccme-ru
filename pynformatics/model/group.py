'''Group model'''
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Text, Float, Unicode
from sqlalchemy.orm import relationship, backref, relation

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from pynformatics.model.meta import Base


class  Group(Base):
    __tablename__ = 'mdl_ejudge_group'
    __table_args__ = {'schema':'moodle'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    description = Column(Unicode)
    owner_id = Column(Integer)
    visible = Column(Integer)

class UserGroup(Base):
    __tablename__ = 'mdl_ejudge_group_users'
    __table_args__ = {'schema':'moodle'}

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    group_id = Column(Integer, ForeignKey('moodle.mdl_ejudge_group.id'))

    group = relationship('Group', backref=backref('user_group', lazy='select'))
    user = relationship('User', backref=backref('user_group', lazy='select'))

    #firstname = association_proxy('user', 'firstname')
    #lastname = association_proxy('user', 'lastname')
    #deleted = association_proxy('user', 'deleted')
    #problems_solved = association_proxy('user', 'problems_solved')
    #ejudge_id = association_proxy('user', 'ejudge_id')
    #city = association_proxy('user', 'city')
    #school = association_proxy('user', 'school')
