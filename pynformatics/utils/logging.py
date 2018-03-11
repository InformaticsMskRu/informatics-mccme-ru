import logging
import transaction

from pynformatics.model.action import Action
from pynformatics.model.log import Log
from pynformatics.models import DBSession


class SQLAlchemyHandler(logging.Handler):
    def emit(self, record):
        user_id = None
        if hasattr(record, 'user'):
            user_id = record.user.id
        elif hasattr(record, 'user_id'):
            user_id = record.user_id

        action_id = Action.get_id(description=record.msg)

        log_fields = {
            'action_id': action_id,
            'user_id': user_id,
            'instance_id': getattr(record, 'instance_id', None),
        }

        log = Log(**log_fields)

        DBSession.add(log)
        DBSession.flush([log])
        transaction.commit()


log = logging.getLogger('db_log')
log.addHandler(SQLAlchemyHandler())


def db_log(msg,
           *,
           level=logging.INFO,
           user=None,
           user_id=None,
           instance_id=None,
           ):
    """
    Логирует действие пользователя в базу
    :param msg: название действия
    :param level:
    :param user:
    :param user_id:
    :param instance_id:
    :return:
    """
    extra = {}
    if user is not None:
        extra['user'] = user
    if user_id is not None:
        extra['user_id'] = user_id
    if instance_id is not None:
        extra['instance_id'] = instance_id
    log.log(level, msg, extra=extra)
