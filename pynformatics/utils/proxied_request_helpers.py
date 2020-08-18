def peek_request_args(request, get_params=None, post_params=None):
    get_params = get_params or []
    post_params = post_params or []

    params = {}
    for param in get_params:
        req_param = request.params.get(param)
        if req_param is not None:
            params[param] = req_param

    body_params = {}
    request_attributes = ['params', 'json_body']
    for param in post_params:
        for attr in request_attributes:
            request_data = getattr(request, attr)
            req_param = request_data.get(param)
            if req_param is not None:
                body_params[param] = req_param
                break

    return params, body_params
