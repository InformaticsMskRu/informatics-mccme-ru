import logging
from gevent import (
    Greenlet,
    sleep
)


log = logging.getLogger('submit_queue')


class SubmitWorker(Greenlet):
    def __init__(self, queue):
        super(SubmitWorker, self).__init__()
        self.queue = queue

    def _run(self):
        while True:
            if not self.queue:
                sleep(1)
                continue
            try:
                submit = self.queue.get()
                submit.send()
                self.queue.total_successful += 1
            except Exception:
                log.exception('Submit worker caught exception and skipped submit without notifying user')
                self.queue.total_failed += 1

            log.info(
                '[GET] size: %s, in: %s, out: %s, failed: %s',
                self.queue.size,
                self.queue.total_in,
                self.queue.total_successful,
                self.queue.total_failed
            )
