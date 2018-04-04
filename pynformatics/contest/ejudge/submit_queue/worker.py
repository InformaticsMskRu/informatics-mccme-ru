import logging
from gevent import Greenlet

log = logging.getLogger('submit_queue')


class SubmitWorker(Greenlet):
    def __init__(self, queue):
        super(SubmitWorker, self).__init__()
        self.queue = queue
        log.info('Submit worker spawned.')

    def handle_submit(self):
        submit = self.queue.get()
        try:
            submit.send()
        except Exception:
            log.exception('Submit worker caught exception and skipped submit without notifying user')

    def _run(self):
        while True:
            self.handle_submit()
