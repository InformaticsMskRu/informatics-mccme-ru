import logging
from gevent.queue import Queue

from .submit import Submit
from .worker import SubmitWorker


log = logging.getLogger('submit_queue')


class SubmitQueue(Queue):
    def __init__(self, workers):
        super(SubmitQueue, self).__init__()
        self.total_in = 0
        self.total_successful = 0
        self.total_failed = 0
        self.workers = [
            SubmitWorker(self)
            for _ in range(workers)
        ]
        for worker in self.workers:
            worker.start()

    @property
    def size(self):
        return self.total_in - self.total_successful - self.total_failed

    def submit(self, context, file, language_id, ejudge_url):
        self.put(
            Submit(
                context=context,
                file=file,
                language_id=language_id,
                ejudge_url=ejudge_url,
            )
        )
        self.total_in += 1
        log.info(
            '[PUT] size: %s, in: %s, out: %s, failed: %s',
            self.size,
            self.total_in,
            self.total_successful,
            self.total_failed
        )
