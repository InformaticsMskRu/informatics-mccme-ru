from gevent import (
    Greenlet,
    sleep
)


class SubmitWorker(Greenlet):
    def __init__(self, queue):
        super(SubmitWorker, self).__init__()
        self.queue = queue

    def _run(self):
        while True:
            if not self.queue:
                sleep(1)
                continue

            submit = self.queue.get()
            try:
                submit.send()
            except Exception:
                raise
