from .queue import SubmitQueue


submit_queue = SubmitQueue()
peek_all_submits = submit_queue.peek_all_submits
peek_user_submits = submit_queue.peek_user_submits
queue_submit = submit_queue.submit