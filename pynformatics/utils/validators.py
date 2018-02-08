from functools import wraps

from pynformatics.utils.exceptions import BadRequest


class Param:
    def __init__(self, name, required=False):
        self.name = name
        self.required = required

    def validate(self, value):
        pass

    def transform(self, value):
        self.validate(value)
        return value


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
    def decorator(view_function):

        @wraps(view_function)
        def wrapper(request):
            data = getattr(request, source)
            for param in params:
                if param.name not in data:
                    if param.required:
                        raise BadRequest(message='Parameter "{}" is required'.format(param.name))
                else:
                    param.validate(data[param.name])
            return view_function(request)
        return wrapper
    return decorator


def validate_params(*params: Param):
    return validate('params', *params)


def validate_matchdict(*params: Param):
    return validate('matchdict', *params)
