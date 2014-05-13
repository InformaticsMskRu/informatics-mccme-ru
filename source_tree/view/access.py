from pyramid.view import view_config

from source_tree.utils.capability import check_capability, check_capability_ex


@view_config(route_name='access', renderer='json')
def access(request):
    res = {}
    for cap in ['user', 'edit', 'admin', 'manage_contest']:
        res[cap] = check_capability_ex(request, cap)
    return res
