import inspect
from functools import wraps

from pynformatics.utils.exceptions import BadRequest


class Param:
    def __init__(self, name, required=False, alias=None):
        self.name = name
        self.required = required
        self.alias = alias

    def validate(self, value):
        pass

    def transform(self, value):
        self.validate(value)
        return value

    def get_alias(self):
        if self.alias:
            return self.alias
        return self.name


class IntParam(Param):
    def validate(self, value):
        super(IntParam, self).validate(value)
        try:
            int(value)
        except:
            raise BadRequest(message='Parameter "{}" must be int'.format(self.name))

    def transform(self, value):
        self.validate(value)
        return int(value)


def validate(source, *params: Param):
    """
    Примеры использования

    @validate_matchdict(IntParam('owner_id', required=True))
    def group_get_owned_by(request, *, owner_id):
        ...

    @validate_params(IntParam('id', required=True, alias='id_from_params'))
    @validate_matchdict(IntParam('id', required=True, alias='id_from_matchdict'))
    def group_get_owned_by(request, *, id_from_params, id_from_matchdict):
        ...

    "*" означает, что дальше идут KEYWORD_ONLY аргументы
    """
    def decorator(view_function):
        @wraps(view_function)
        def wrapper(request, *args, **kwargs):
            view_function_keywords_names = map(lambda x: x.name, filter(
                lambda v: v.kind == v.KEYWORD_ONLY,  # KEYWORD_ONLY это те которые после *args или *
                inspect.signature(view_function).parameters.values()
            ))
            data = getattr(request, source)
            for param in params:
                if param.name not in data:
                    if param.required:
                        raise BadRequest(message='Parameter "{}" is required'.format(param.name))
                else:
                    param.validate(data[param.name])
                    if param.get_alias() in view_function_keywords_names:
                        kwargs[param.get_alias()] = param.transform(data[param.name])
            return view_function(request, *args, **kwargs)
        return wrapper
    return decorator


def validate_params(*params: Param):
    return validate('params', *params)


def validate_matchdict(*params: Param):
    return validate('matchdict', *params)


def validate_json(*params: Param):
    return validate('json', *params)
