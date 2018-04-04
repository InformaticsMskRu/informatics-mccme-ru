from redis import (
    ConnectionPool,
    StrictRedis,
)


redis = StrictRedis(host=None, port=None, db=None)


def init_redis(settings):
    redis.connection_pool = ConnectionPool(
        host=settings['redis.host'],
        port=settings['redis.port'],
        db=settings['redis.db'],
    )
