import logging
import traceback
from pyramid.view import exception_view_config

from pynformatics.utils.exceptions import (
    BaseApiException,
    InternalServerError,
)


log = logging.getLogger(__name__)


@exception_view_config(BaseApiException, renderer='json')
def api_exception_handler(exception, request):
    if isinstance(exception, InternalServerError):
        log.error('Internal Server Error message: %s' % exception.error)
        log.error(traceback.format_exc())

    request.response.status_code = exception.code
    return {
        'code': exception.code,
        'message': exception.message,
    }
