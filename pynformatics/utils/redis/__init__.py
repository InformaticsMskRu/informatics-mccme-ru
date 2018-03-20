from redis import StrictRedis


class RedisWrapper:
    def __init__(self):
        self.redis = None

    def configure(self, host, port, db):
        self.redis = StrictRedis(host=host, port=port, db=db)

    def __getattr__(self, item):
        return getattr(self.redis, item)


redis = RedisWrapper()


def init_redis(settings):
    redis.configure(
        host=settings['redis.host'],
        port=settings['redis.port'],
        db=settings['redis.db'],
    )
