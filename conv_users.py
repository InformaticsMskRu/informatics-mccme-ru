from datetime import datetime
from pyramid.paster import get_appsettings
from pyramid.config import Configurator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String, Unicode, Boolean, DateTime
from sqlalchemy import ForeignKey, Column
from sqlalchemy import engine_from_config
from sqlalchemy.orm import (
    sessionmaker,
)


DBSession = sessionmaker()

settings = get_appsettings('dev-source.ini', 'main')
engine = engine_from_config(settings, 'sqlalchemy.')
DBSession.configure(bind=engine)

Base = declarative_base()

Base.metadata.bind = engine
db_session = DBSession()


class Logins(Base):
    __tablename__ = "logins"
    __table_args__ = {"schema": "ejudge"}
    login = Column(Unicode)
    password = Column(Unicode)
    user_id = Column(Integer, primary_key=True)

    
class UserEjudge(Base):
    __tablename__ = "mdl_user_ejudge"
    __table_args__ = {"schema": "moodle"}
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    login = Column(Unicode)
    password = Column(Unicode)
    ejudge_id = Column(Integer)

    def __init__(self, user_id=0, login='', password='', ejudge_id=0):
        self.id = user_id
        self.user_id = user_id
        self.login = login
        self.password = password
        self.ejudge_id = ejudge_id

users = db_session.query(UserEjudge).order_by(UserEjudge.id).all()
cur_id = users[-1].id
logins = db_session.query(Logins).filter(Logins.login.like('m0%')).all()

for login in logins:
    cur_id += 1
    db_session.add(UserEjudge(
        user_id=cur_id,
        login=login.login,
        password=login.password,
        ejudge_id=login.user_id
    ))
db_session.commit()

'''logins_d = [{
        'user_id': login.user_id,
        'login': login.login
    } 
    for login in logins[0:20]]
'''

