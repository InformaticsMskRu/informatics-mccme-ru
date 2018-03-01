import short_url


class UrlGenerator:
    def __init__(self, secret=0):
        self._secret = secret

    def decode(self, arg):
        raise NotImplementedError

    def encode(self, url):
        raise NotImplementedError


class IntUrlGenerator(UrlGenerator):
    def encode(self, n: int):
        return short_url.encode_url(n ^ self._secret)

    def decode(self, url):
        return short_url.decode_url(url) ^ self._secret
