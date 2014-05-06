from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode, Boolean, DateTime
from sqlalchemy.orm import relationship, backref, relation
from datetime import datetime

from source_tree.models import Problem
from source_tree.models import Base
from source_tree.models import SimpleUser

class Source(Base):
    __tablename__ = 'mdl_sources'
    __table_args__ = {'schema':'moodle'}    
    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    parent_id = Column(Integer, ForeignKey('moodle.mdl_sources.id'))
    order = Column(Integer)
    problem_id = Column(Integer, ForeignKey('moodle.mdl_problems.id'))
    verified = Column(Boolean)
    author = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    time = Column(DateTime)

    children = relationship(
        'Source', 
        backref=backref('parent', remote_side=[id]), 
        order_by=order,
        lazy='dynamic'
    )
    
    problem = relationship('Problem', backref='source')
    user = relationship('SimpleUser')

    def __init__(self, name='', parent_id=0, order=1000, problem_id=0, author=0, verified=True):
        self.name = name
        self.parent_id = parent_id
        self.order = order
        self.problem_id = problem_id
        self.verified = verified
        self.author = author
        self.time = datetime.now()

    def __json__(self, request):
        return {
            'id': self.id, 
            'name': self.name, 
            'parent_id': self.parent_id,
            'order': self.order,
            'problem_id': self.problem_id,
            'verified': self.verified,
            'author': self.author,
            'time': self.time.isoformat(sep=' '),
            'is_leaf': not self.children.first()
        }

    def get_type(self):
        if not self.parent:
            return "_none"
        elif self.parent.parent:
            return self.parent.get_type()
        else:
            return self.name
    
    def is_root(self):
        return self.parent_id == 1
            
    def get_path(self):
        result = self.parent.get_path() if self.parent else []
        result.append(self)
        return result

    def get_source_path(self):
        if self.parent:
            result = self.parent.get_source_path()
        else:
            result = []
        result.append(self.name)
        return result
