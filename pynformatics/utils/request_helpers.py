import functools

import requests


RECAPTCHA_URL = "https://www.google.com/recaptcha/api/siteverify"


def check_captcha(resp, secret):
    params = {
       'secret': secret,
       'response': resp
    }

    r = requests.get(RECAPTCHA_URL, params=params)
    return r.json().get("success", False)


def require_captcha(f):
    @functools.wraps(f)
    def wrapper(request, *args, **kwargs):
        recaptha_resp = request.params['g-recaptcha-response']
        if not check_captcha(recaptha_resp, request.registry.settings["recaptcha.secret"]):
            return "Не получилось"
        return f(request, *args, **kwargs)
    return wrapper
