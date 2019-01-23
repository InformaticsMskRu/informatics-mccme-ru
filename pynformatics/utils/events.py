from pynformatics import DBSession


def rollback_on_request_finished(_):
    # не известно, работает ли это
    DBSession().rollback()


def subscribe_rollback_on_request_finished(request):
    request.request.add_finished_callback(rollback_on_request_finished)
