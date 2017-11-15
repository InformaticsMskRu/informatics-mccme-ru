from pyramid.view import exception_view_config
from pyramid.response import Response
from pynformatics.utils.exceptions import BaseApiException


@exception_view_config(BaseApiException, renderer='json')
def api_exception_handler(exception, request):
    request.response.status_code = exception.code
    return {
        'code': exception.code,
        'message': exception.message,
    }
