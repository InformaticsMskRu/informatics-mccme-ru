import logging
from gevent import (
    Greenlet,
    sleep
)


log = logging.getLogger(__name__)


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
            except Exception:
                log.exception('Submit worker caught exception and skipped submit without notifying user')
