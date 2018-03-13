import json
import logging
from collections import defaultdict
from gevent.queue import Queue


log = logging.getLogger(__name__)

_clients = defaultdict(list)


class Client:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self._queue = Queue()

        _clients[user_id].append(self)
        log.debug('New client created for user %s', user_id)

    def has_notification(self):
        return not self._queue.empty()

    def get_notification(self):
        return json.dumps(self._queue.get(), separators=(',',':'))

    def notify(self, data):
        self._queue.put(data)

    def disconnect(self):
        client_index = next(
            index
            for index, client in enumerate(_clients[self.user_id])
            if client is self
        )
        _clients[self.user_id].pop(client_index)


def notify_user(user_id,
                data=None,
                runs=None,

                ):
    data = data or {}
    if runs:
        data['runs'] = runs

    user_clients = _clients[user_id]
    for client in user_clients:
        log.debug('Client of user %s is being notified', user_id)
        client.notify(data)
