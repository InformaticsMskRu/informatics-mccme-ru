import pickle

from pynformatics.utils.redis import redis


class RedisQueue:
    def __init__(self, key):
        self.key = key

    def put(self, value, pipe=None):
        if pipe is None:
            pipe = redis

        pipe.rpush(self.key, pickle.dumps(value))

    def get(self, pipe=None):
        if pipe is None:
            pipe = redis

        value = pipe.lpop(self.key)
        if value:
            value = pickle.loads(value)
        return value

    def get_blocking(self, timeout=0, pipe=None):
        if pipe is None:
            pipe = redis

        value = pipe.blpop(self.key, timeout=timeout)
        if value:
            value = pickle.loads(value[1])
        return value
