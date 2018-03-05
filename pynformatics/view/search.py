from pyramid.view import view_config
from pynformatics import User
from pynformatics.utils.context import with_context
from pynformatics.utils.exceptions import (
    SearchQueryIsEmpty,
    PaginationPageOutOfRange,
    PaginationPageSizeNegativeOrZero
)
from pynformatics.utils.validators import (
    validate_params,
    Param,
    IntParam
)

PAGE_SIZE = 20


@view_config(route_name='search.user', request_method='GET', renderer='json')
@validate_params(Param('query', required=True), IntParam('page_size'), IntParam('page'))
@with_context
def search_user(request, context):
    search_string = request.params['query']
    search_string = search_string.strip()
    if not search_string:
        raise SearchQueryIsEmpty
    page = int(request.params.get('page', 0))
    page_size = int(request.params.get('page_size', PAGE_SIZE))

    if page_size < 1:
        raise PaginationPageSizeNegativeOrZero

    users = User.search_by_string(search_string)

    users_count = users.count()
    pages_total = users_count // page_size
    if page > pages_total or page < 0:
        raise PaginationPageOutOfRange

    fetched_users = users.slice(page * page_size, (page + 1) * page_size).all()

    return {
        'data': [
            user.serialize(
                context=context,
                attributes=('id', 'username', 'lastname', 'firstname', 'email')
            )
            for user in fetched_users
        ],
        'records_total': users_count,
        'page': page,
        'page_size': page_size,
        'pages_total': pages_total,
    }
