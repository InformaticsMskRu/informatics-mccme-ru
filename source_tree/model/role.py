from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relationship

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
    role_id = Column('roleid', Integer, ForeignKey('moodle.mdl_role.id'))
    context_id = Column('contextid', Integer, ForeignKey('moodle.mdl_context.id'))
    user_id = Column('userid', Integer, ForeignKey('moodle.mdl_user.id'))


    role = relationship('Role', lazy='joined')
    context = relationship('Context', lazy='joined')
