import hashlib


def attrs_to_dict(obj, *attrs):
    return {
        attr: getattr(obj, attr, None)
        for attr in attrs
    }


def check_password(password, hashed_password):
    md5 = hashlib.md5()
    md5.update(password.encode('utf-8'))
    return md5.hexdigest() == hashed_password
