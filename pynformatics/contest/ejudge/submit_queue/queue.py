from gevent.queue import Queue

from .submit import Submit
from .worker import SubmitWorker


class SubmitQueue(Queue):
    def __init__(self, workers):
        super(SubmitQueue, self).__init__()
        self.workers = [
            SubmitWorker(self)
            for _ in range(workers)
        ]
        for worker in self.workers:
            worker.start()

    def submit(self, context, file, language_id, ejudge_url):
        self.put(
            Submit(
                context=context,
                file=file,
                language_id=language_id,
                ejudge_url=ejudge_url,
            )
        )
