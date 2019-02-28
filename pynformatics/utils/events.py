from pynformatics.models import DBSession


def rollback_on_request_finished(_):
    # не известно, работает ли это
    if DBSession.is_active:
        DBSession.rollback()


def subscribe_rollback_on_request_finished(request):
    request.request.add_finished_callback(rollback_on_request_finished)
