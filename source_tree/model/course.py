from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode, Boolean, DateTime
from sqlalchemy.orm import relationship, backref, relation
from datetime import datetime

from source_tree.models import Base, SimpleUser


class CourseRaw(Base):
    __tablename__ = 'mdl_course'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    fullname = Column(Unicode)
    shortname = Column(Unicode)
    password = Column(Unicode)
    visible = Column(Boolean)
    category = Column(Integer)


class Course(Base):
    __tablename__ = 'mdl_course_tree'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    name = Column(Unicode)
    parent_id = Column(Integer, ForeignKey('moodle.mdl_course_tree.id'))
    order = Column(Integer)
    course_id = Column(Integer, ForeignKey('moodle.mdl_course.id'))
    visible = Column(Boolean)
    collapsed = Column(Boolean)
    verified = Column(Boolean)
    author = Column(Integer, ForeignKey('moodle.mdl_user.id'))
    time = Column(DateTime)
    displayed = Column(Boolean)

    children = relationship(
        'Course', 
        backref=backref('parent', remote_side=[id]), 
        order_by=order,
        lazy='dynamic'
    )
    course = relationship('CourseRaw', lazy='joined')
    user = relationship('SimpleUser', lazy='joined')

    def __init__(self, name='', parent_id=0, order=0, course_id=0, author=0, 
            visible=True, collapsed=False, verified=True, displayed=False):
        self.name = name
        self.parent_id = parent_id
        self.order = order
        self.course_id = course_id
        self.visible = visible
        self.collapsed = collapsed
        self.verified = verified
        self.author = author
        self.time = datetime.now() 
        self.displayed = displayed

    def __json__(self, request):
        return {
            'id': self.id,
            'name': self.name,
            'full_name': self.full_name(),
            'parent_id': self.parent_id,
            'author': self.author,
            'order': self.order,
            'course_id': self.course_id,
            'course_name': self.course.fullname if self.course else None,
            'verified': self.verified,
            'visible': self.visible,
            'collapsed': self.collapsed,
            'is_leaf': not self.children.first(),
            'time': self.time.isoformat(sep=' '),
            'displayed': self.displayed,
        }

    def is_root(self):
        return self.parent_id == 1

    def full_name(self):
        if self.id == 1:
            return ""
        res = ""
        if not self.is_root() and self.parent:
            res += self.parent.full_name() + " -> "
        res += self.name
        return res

    def parents(self):
        if self.id == 1:
            return []
        elif self.is_root() or not self.parent:
            return [self.id]
        else:
            return self.parent.parents() + [self.id]

    def get_subtree_nodes(self):
        res = [self]
        for child in self.children:
            res += child.get_subtree_nodes()
        return res

        
class CourseTreeCap(Base):
    __tablename__ = 'mdl_course_tree_cap'
    __table_args__ = {'schema': 'moodle'}

    id = Column(Integer, primary_key=True)
    node_id = Column(Integer)
    user_id = Column(Integer)
    value = Column(Integer)

    def __init__(self, node_id=0, user_id=0, value=0):
        self.node_id = node_id
        self.user_id = user_id
        self.value = value
