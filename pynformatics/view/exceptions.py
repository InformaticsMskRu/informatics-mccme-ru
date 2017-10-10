from pyramid.view import exception_view_config
from pynformatics.utils.exceptions import BaseApiException


@exception_view_config(BaseApiException, renderer='json')
def api_exception_handler(exception, request):
    return {
        'error': {
            'code': exception.code,
            'message': exception.message,
        }
    }
