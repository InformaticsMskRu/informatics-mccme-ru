import pickle
import uuid

from pynformatics.utils.redis import redis
import sqlalchemy


def client_channel(client_uuid):
    return f'notify:client:{client_uuid}'


def user_channel(user_id):
    return f'notify:user:{user_id}'


class Client:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.uuid = str(uuid.uuid4())
        self.pubsub = redis.pubsub()
        self.pubsub.subscribe(client_channel(self.uuid))
        if user_id:
            self.pubsub.subscribe(user_channel(user_id))

    def get_message(self):
        message = None
        while True:
            message = self.pubsub.get_message()
            if not (message and message['type'] == 'subscribe'):
                break
        if message:
            message = pickle.loads(message['data'])
        return message


def format_message(message=None,
                   meta=None,
                   runs=None,
                   event=None,
                   ):
    message = message or {}
    if meta:
        message['meta'] = meta
    if runs:
        message['runs'] = runs
    if event:
        message['event'] = event
    return message


def notify_client(client_uuid, **kwargs):
    message = format_message(**kwargs)
    redis.publish(client_channel(client_uuid), pickle.dumps(message))


def notify_user(user_id, **kwargs):
    message = format_message(**kwargs)
    redis.publish(user_channel(user_id), pickle.dumps(message))
