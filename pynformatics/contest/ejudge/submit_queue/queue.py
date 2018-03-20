import logging

from .submit import Submit
from .worker import SubmitWorker
from pynformatics.utils.redis.queue import RedisQueue


log = logging.getLogger('submit_queue')


DEFAULT_SUBMIT_QUEUE = 'submit.queue'


class SubmitQueue(RedisQueue):
    def __init__(self, key=DEFAULT_SUBMIT_QUEUE):
        super(SubmitQueue, self).__init__(key=key)
        self.total_in = 0
        self.total_successful = 0
        self.total_failed = 0
        # self.workers = [
        #     SubmitWorker(self)
        #     for _ in range(workers)
        # ]
        # for worker in self.workers:
        #     worker.start()

    @property
    def size(self):
        return self.total_in - self.total_successful - self.total_failed

    def submit(self, context, file, language_id, ejudge_url):
        submit = Submit(
            context=context,
            file=file,
            language_id=language_id,
            ejudge_url=ejudge_url,
        )
        self.put(submit.encode())

        self.total_in += 1
        log.info(
            '[PUT] size: %s, in: %s, out: %s, failed: %s',
            self.size,
            self.total_in,
            self.total_successful,
            self.total_failed
        )

    def get(self):
        submit_encoded = super(SubmitQueue, self).get_blocking()
        return Submit.decode(submit_encoded)