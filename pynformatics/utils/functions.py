import hashlib
import random


def attrs_to_dict(obj, *attrs):
    return {
        attr: getattr(obj, attr, None)
        for attr in attrs
    }


def random_password(length):
    SYMBOLS = 'poiuytrewqlkjhgfdsmnbvcxzQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
    return ''.join([random.choice(SYMBOLS) for i in range(length)])


def hash_password(password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest()


def check_password(password, hashed_password):
    return hash_password(password) == hashed_password


def index_of(iterable, predicate, default=None):
    return next(
        (
            index
            for (index, element) in enumerate(iterable)
            if predicate(element)
        ),
        default
    )
