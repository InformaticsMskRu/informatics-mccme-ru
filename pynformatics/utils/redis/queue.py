import pickle

from pynformatics.utils.redis import redis


class RedisQueue:
    def __init__(self, key):
        self.key = key

    def put(self, value):
        redis.rpush(self.key, pickle.dumps(value))

    def get(self):
        value = redis.lpop(self.key)
        if value:
            value = pickle.loads(value)
        return value

    def get_blocking(self, timeout=0):
        value = redis.blpop(self.key, timeout=timeout)
        if value:
            value = pickle.loads(value[1])
        return value
