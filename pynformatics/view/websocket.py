import gevent
import json
import logging
import uwsgi
from pyramid.view import view_config

from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import BadRequest
from pynformatics.utils.notify import (
    Client,
    notify_client,
)


log = logging.getLogger(__name__)


def is_websocket(request):
    return (
        'websocket' in request.environ.get('HTTP_UPGRADE', '').lower() and
        'upgrade' in request.environ.get('HTTP_CONNECTION', '').lower()
    )


@view_config(route_name='websocket', renderer='string')
@with_context
def websocket(request, context):
    if not is_websocket(request):
        raise BadRequest

    uwsgi.websocket_handshake(
        request.environ['HTTP_SEC_WEBSOCKET_KEY'],
        request.environ.get('HTTP_ORIGIN', ''),
    )
    websocket_fd = uwsgi.connection_fd()

    client = Client(user_id=context.user.id)
    notify_client(client.uuid, meta={'client_uuid': client.uuid})

    while True:
        ready = gevent.select.select([websocket_fd], [], [], 4.0)
        if not ready[0]:
            uwsgi.websocket_recv_nb()

        for fd in ready[0]:
            if fd == websocket_fd:
                try:
                    message = uwsgi.websocket_recv_nb()
                except IOError:
                    # TODO: использовать очередь (redis etc.) и вынести websocket на отдельный инстанс
                    # Дисконнект веб-сокета вызывает ошибку из-за того, что pyramid пытается задать хедеры второй раз
                    # https://github.com/miguelgrinberg/Flask-SocketIO/issues/377
                    return ''
                if message:
                    pass

        message = client.get_message()
        while message is not None:
            log.info('sending message %s', message)
            uwsgi.websocket_send(json.dumps(message, separators=(',', ':')))
            message = client.get_message()
