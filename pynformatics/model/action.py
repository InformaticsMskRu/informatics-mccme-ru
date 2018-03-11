from sqlalchemy import Column
from sqlalchemy.types import (
    Integer,
    String,
)

from pynformatics.model.meta import Base
from pynformatics.models import DBSession


class Action(Base):
    __table_args__ = {'schema': 'pynformatics'}
    __tablename__ = 'action'

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String)

    @staticmethod
    def get_id(description):
        '''
        Возвращает action_id по описанию действия.
        В случае, если такого действия нет, создает его.
        '''
        description = description.upper()
        instance = DBSession.query(Action).filter_by(description=description).first()
        if not instance:
            instance = Action(description=description)
            DBSession.add(instance)
            DBSession.flush([instance])
        return instance.id
