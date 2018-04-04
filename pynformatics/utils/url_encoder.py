import short_url


_instance = None


def init_url_encoder(settings):
    global _instance
    _instance = short_url.UrlEncoder(
        alphabet=settings.get('url_encoder.alphabet')
    )


def encode(n):
    return _instance.encode_url(n)


def decode(url):
    return _instance.decode_url(url)
