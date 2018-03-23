import logging

from .submit import Submit
from .worker import SubmitWorker
from pynformatics.utils.redis.queue import RedisQueue


log = logging.getLogger('submit_queue')


DEFAULT_SUBMIT_QUEUE = 'submit.queue'


class SubmitQueue(RedisQueue):
    def __init__(self, key=DEFAULT_SUBMIT_QUEUE):
        super(SubmitQueue, self).__init__(key=key)

    def submit(self, context, file, language_id, ejudge_url):
        submit = Submit(
            context=context,
            file=file,
            language_id=language_id,
            ejudge_url=ejudge_url,
        )
        self.put(submit.encode())

    def get(self):
        submit_encoded = super(SubmitQueue, self).get_blocking()
        return Submit.decode(submit_encoded)
