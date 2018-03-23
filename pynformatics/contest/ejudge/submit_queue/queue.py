import datetime
import logging
import pickle
from redis import WatchError

from .submit import Submit
from .worker import SubmitWorker
from pynformatics.utils.redis import redis
from pynformatics.utils.redis.queue import RedisQueue


log = logging.getLogger('submit_queue')


DEFAULT_SUBMIT_QUEUE = 'submit.queue'


def last_put_id_key(key):
    return f'{key}:last.put.id'


def last_get_id_key(key):
    return f'{key}:last.get.id'


def user_submits_key(key, user_id):
    return f'{key}:user:{user_id}'


class SubmitQueue(RedisQueue):
    """
    Очередь сабмитов. 
    Кроме самих сабмитов поддерживает id последнего добавленного в очередь и 
    id последнего полученного из очереди.
    """

    def __init__(self, key=DEFAULT_SUBMIT_QUEUE):
        super(SubmitQueue, self).__init__(key=key)

    def submit(self, context, file, language_id, ejudge_url):  
        def _submit(pipe):
            submit = Submit(
                id=pipe.incr(last_put_id_key(self.key)),
                context=context,
                create_time=datetime.datetime.now(),
                file=file,
                language_id=language_id,
                ejudge_url=ejudge_url,
            )
            self.put(submit.encode(), pipe=pipe)
            redis.hset(
                user_submits_key(self.key, context.user.id), 
                submit.id, 
                pickle.dumps(submit.encode())
            )
            return submit
        submit = redis.transaction(
            _submit, 
            self.key, 
            last_put_id_key(self.key), 
            value_from_callable=True
        )
        return submit


    def get(self):
        def _get(pipe):
            submit_encoded = super(SubmitQueue, self).get_blocking(pipe=pipe)
            submit = Submit.decode(submit_encoded)
            pipe.set(last_get_id_key(self.key), submit.id)
            return submit
        
        submit = redis.transaction(
            _get, 
            self.key, 
            last_get_id_key(self.key),
            value_from_callable=True,
        )

        redis.hdel(user_submits_key(self.key, submit.user.id), submit.id)
        return submit
    
    def peek_all_submits(self):        
        return [
            Submit.decode(pickle.loads(encoded))
            for encoded in redis.lrange(self.key, 0, -1)
        ]
    
    def peek_user_submits(self, user_id):
        return [
            Submit.decode(pickle.loads(encoded))
            for encoded in redis.hgetall(user_submits_key(self.key, user_id)).values()
        ]
