import logging
from gevent.queue import Queue

from .submit import Submit
from .worker import SubmitWorker


log = logging.getLogger('submit_queue')


class SubmitQueue(Queue):
    def __init__(self, workers):
        super(SubmitQueue, self).__init__()
        self.total_in = 0
        self.workers = [
            SubmitWorker(self)
            for _ in range(workers)
        ]
        for worker in self.workers:
            worker.start()

    @property
    def total_out(self):
        return sum([worker.submitted for worker in self.workers])

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
        log.info('Current size: %s. Total submitted: %s.', self.total_in - self.total_out, self.total_out)
