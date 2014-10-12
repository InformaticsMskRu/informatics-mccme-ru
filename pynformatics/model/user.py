"""User model"""
from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, relation
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection

from pynformatics.model.statement import StatementUser

from pynformatics.model.meta import Base

def lazy(func):
        """ A decorator function designed to wrap attributes that need to be
        generated, but will not change. This is useful if the attribute is  
        used a lot, but also often never used, as it gives us speed in both
        situations."""
        def cached(self, *args):
                name = "_"+func.__name__
                try:
                        return getattr(self, name)
                except AttributeError:
                        value = func(self, *args)
                        setattr(self, name, value)
                        return value
        return cached

class SimpleUser(Base):
    __tablename__ = "mdl_user"
    __table_args__ = {'schema':'moodle'}
#    __mapper_args__ = {'polymorphic_on': discriminator}    
    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    login = Column('ej_login', Unicode)
    password = Column('ej_password', Unicode)
    deleted  = Column('deleted', Boolean)
    ejudge_id = Column('ej_id', Integer)
    problems_solved = Column(Integer)
    statement = relationship("Statement", secondary=StatementUser.__table__, backref=backref("StatementUsers1"), lazy="dynamic")
    statements = association_proxy("StatementUsers2", 'statement')    


class User(SimpleUser):
    __mapper_args__ = {'polymorphic_identity': 'user'}
    username = Column(Unicode)
    email = Column(Unicode)
    city = Column(Unicode)
    school = Column(Unicode)
#    ejudge_users = relation('EjudgeUser', backref="moodle.mdl_user", uselist=False)
#    ejudge_user = relation('EjudgeUser', backref = backref('moodle.mdl_user'), uselist=False, primaryjoin = "EjudgeUser.user_id == User.id")
    
    def __init__(self, id, username='', firstname='', lastname='', email='', city=''):
        self.id = id
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.city = city

    @lazy      
    def _get_current_olymp(self): 
        return None

class PynformaticsUser(User):
    __tablename__ = "mdl_user_settings"
    __table_args__ = {'schema' : 'moodle'}
    __mapper_args__ = {'polymorphic_identity': 'pynformaticsuser'}
    
    id = Column(Integer, ForeignKey('moodle.mdl_user.id'), primary_key=True)
    main_page_settings = Column(Unicode)

#    def __repr__(self):
#        return "<Person(%s, '%s', '%s', '%s', '%s')" % (self.id, self.username, self.firstname, self.lastname, self.email, self.city)


class EjudgeUser(User):
    __tablename__ = "mdl_user_ejudge"
    __table_args__ = {'schema':'moodle'}
    __mapper_args__ = {'polymorphic_identity': 'ejudgeuser'}

    id = Column(Integer, ForeignKey('moodle.mdl_user.id'), primary_key=True)
    login = Column(Unicode)
    password = Column(Unicode)
    ejudge_id = Column(Integer)
    problems_solved = Column(Integer)
#    statement = relationship("Statement", secondary=StatementUser.__table__, backref=backref("StatementUsers1"), lazy="dynamic")
#    statements = association_proxy("StatementUsers2", 'statement')    
        
