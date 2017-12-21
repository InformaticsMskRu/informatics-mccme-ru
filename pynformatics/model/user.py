from typing import Callable

from sqlalchemy import ForeignKey, Column, or_, and_
from sqlalchemy.types import Integer, Unicode, Boolean
from sqlalchemy.orm import relationship, backref, Query
from sqlalchemy.ext.associationproxy import association_proxy
from pynformatics.model.meta import Base
from pynformatics.model.statement import StatementUser
from pynformatics.model.participant import Participant
from pynformatics.models import DBSession
from pynformatics.utils.functions import attrs_to_dict


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
    __table_args__ = {'schema': 'moodle'}
#    __mapper_args__ = {'polymorphic_on': discriminator}    
    id = Column(Integer, primary_key=True)
    firstname = Column(Unicode)
    lastname = Column(Unicode)
    login = Column('ej_login', Unicode)
    password = Column('ej_password', Unicode)
    deleted = Column('deleted', Boolean)
    ejudge_id = Column('ej_id', Integer)
    problems_solved = Column(Integer)
    statement = relationship("Statement", secondary=StatementUser.__table__,
                             backref=backref("StatementUsers1"), lazy="dynamic")
    statements = association_proxy("StatementUsers2", 'statement')

    password_md5 = Column('password', Unicode)

    def get_active_participant(self):
        """
        Возвращает последний participant, если он еще не закончен
        """
        latest_participant = DBSession.query(Participant).filter(
            Participant.user_id == self.id
        ).order_by(
            Participant.id.desc()
        ).first()
        if latest_participant and not latest_participant.finished():
            return latest_participant
        return None

    def serialize(self, context=None, attributes=('id', 'firstname', 'lastname', 'active_virtual')):
        serialized = attrs_to_dict(self, *attributes)
        if 'active_virtual' in attributes:  # TODO Убрать во внешний сериалайзер
            participant = self.get_active_participant()
            if participant:
                serialized['active_virtual'] = participant.serialize(context)
            else:
                serialized.pop('active_virtual')
        return serialized


class User(SimpleUser):
    __mapper_args__ = {'polymorphic_identity': 'user'}
    username = Column(Unicode)
    email = Column(Unicode)
    city = Column(Unicode)
    school = Column(Unicode)
    problems_week_solved = Column(Unicode)

    @classmethod
    def search(cls, filter_func: Callable[[Query], Query], filter_deleted=True):
        if filter_deleted:
            users_query = filter_func(DBSession.query(cls).filter(cls.deleted == False))
        else:
            users_query = filter_func(DBSession.query(cls))
        return users_query

    @classmethod
    def search_by_string(cls, search_string):
        def filter_func(query: Query):
            if search_string.count(' '):
                str1, str2 = search_string.split(' ', 1)
                query = query.filter(or_(
                    and_(cls.firstname.like("%{}%".format(str1)), cls.lastname.like("%{}%".format(str2))),
                    and_(cls.lastname.like("%{}%".format(str1)), cls.firstname.like("%{}%".format(str2))),
                ))
            else:
                query = query.filter(or_(
                    cls.email.like("%{}%".format(search_string)),
                    cls.username.like("%{}%".format(search_string)),
                    cls.firstname.like("%{}%".format(search_string)),
                    cls.lastname.like("%{}%".format(search_string)),
                ))
            return query

        return cls.search(filter_func)

    @lazy
    def _get_current_olymp(self): 
        return None


class PynformaticsUser(User):
    __tablename__ = "mdl_user_settings"
    __table_args__ = {'schema': 'moodle'}
    __mapper_args__ = {'polymorphic_identity': 'pynformaticsuser'}
    
    id = Column(Integer, ForeignKey('moodle.mdl_user.id'), primary_key=True)
    main_page_settings = Column(Unicode)

#    def __repr__(self):
#        return "<Person(%s, '%s', '%s', '%s', '%s')" % (self.id, self.username, self.firstname, self.lastname, self.email, self.city)


# TODO: поправить SAWarning. Нужно ли наследование от User? Если да, можно убрать id
# class EjudgeUser(User):
#     __tablename__ = "mdl_user_ejudge"
#     __table_args__ = {'schema':'moodle'}
#     __mapper_args__ = {'polymorphic_identity': 'ejudgeuser'}
#
#     id = Column(Integer, ForeignKey('moodle.mdl_user.id'), primary_key=True)
#     ejudge_login = Column(Unicode)
#     ejudge_password = Column(Unicode)
#     ejudge_id = Column(Integer)
#     ejudge_problems_solved = Column(Integer)
#    statement = relationship("Statement", secondary=StatementUser.__table__, backref=backref("StatementUsers1"), lazy="dynamic")
#    statements = association_proxy("StatementUsers2", 'statement')
