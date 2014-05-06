from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode, Boolean, DateTime
from sqlalchemy.orm import relationship, backref, relation
from datetime import datetime

from source_tree.models import Base


class Role(Base):
    __tablename__ = 'mdl_role'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    shortname = Column(Unicode)
    description = Column(Unicode)
    sortorder = Column(Integer)

    
class Context(Base):
    __tablename__ = 'mdl_context'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    contextlevel = Column(Integer)
    instanceid = Column(Integer)

    
class RoleAssignment(Base):
    __tablename__ = 'mdl_role_assignments'
    __table_args__ = {'schema': 'moodle'}
    
    id = Column(Integer, primary_key=True)
    roleid = Column(Integer, ForeignKey("moodle.mdl_role.id"))
    contextid = Column(Integer, ForeignKey("moodle.mdl_context.id"))
    userid = Column(Integer, ForeignKey("moodle.mdl_user.id"))

    role = relationship('Role', lazy='joined')
    context = relationship('Context', lazy='joined')
