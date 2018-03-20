from hamcrest import (
    assert_that,
    equal_to,
)

from pynformatics.testutils import TestCase
from pynformatics.utils.redis.queue import RedisQueue


class TestUtils__redis_queue(TestCase):
    def setUp(self):
        super(TestUtils__redis_queue, self).setUp()

    def test_put_get(self):
        queue = RedisQueue(key='test_queue')

        queue.put(179)
        queue.put('test')
        queue.put('тест')

        gets = [
            queue.get()
            for _ in range(4)
        ]
        assert_that(gets, equal_to([179, 'test', 'тест', None]))

    def test_put_get_blocking(self):
        queue = RedisQueue(key='test_queue')

        queue.put('test')
        gets = [
            queue.get_blocking(),
            queue.get_blocking(timeout=1)
        ]
        assert_that(gets, equal_to(['test', None]))


