def attrs_to_dict(obj, *attrs):
    return {
        attr: getattr(obj, attr, None)
        for attr in attrs
    }
