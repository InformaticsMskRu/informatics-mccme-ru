from .queue import SubmitQueue


submit_queue = None
queue_submit = None


def init_submit_queue(settings):
    global submit_queue, queue_submit

    submit_queue = SubmitQueue(int(settings['submit_queue.workers']))
    queue_submit = submit_queue.submit
