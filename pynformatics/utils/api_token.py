"""Bearer-token authorization for the /api/v1 endpoints.

Tokens come from the "api.tokens" setting (config.secret JSON):

    {"id": 7, "name": "bot1", "sha256": "<hex sha256 of the token>",
     "user_ids": [101, 102] | null, "problems": [1, 2] | null}

null in "user_ids" / "problems" means "any". Both keys are required, so a typo
can't silently widen a token.
"""
import hashlib
import re
from hmac import compare_digest

from pyramid.response import Response

# Far from DEFAULT_MOODLE_CONTEXT_SOURCE (10) and CONTEXT_SHIFT + course_id
API_CONTEXT_BASE = 10_000_000

# Moodle ids up to 2 are the guest and the system users
MIN_USER_ID = 3

_SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


class ApiToken:
    def __init__(self, id, name, sha256, user_ids, problems):
        self.id = id
        self.name = name
        self.sha256 = sha256
        self.user_ids = user_ids
        self.problems = problems

    @property
    def context_source(self):
        return API_CONTEXT_BASE + self.id

    def allows_user(self, user_id):
        return user_id >= MIN_USER_ID and (self.user_ids is None or user_id in self.user_ids)

    def allows_problem(self, problem_id):
        return self.problems is None or problem_id in self.problems


def _int_list_or_none(entry, key):
    if key not in entry:
        raise ValueError('api.tokens: token {!r} has no "{}" (use null for any)'.format(entry.get('id'), key))
    value = entry[key]
    if value is None:
        return None
    if not isinstance(value, list) or not all(isinstance(v, int) and not isinstance(v, bool) for v in value):
        raise ValueError('api.tokens: "{}" must be null or a list of integers'.format(key))
    return value


def parse_api_tokens(settings):
    """Validate the "api.tokens" setting; raises ValueError on a bad entry."""
    raw = settings.get('api.tokens') or []
    if not isinstance(raw, list):
        raise ValueError('api.tokens must be a list')

    tokens = []
    seen_ids = set()
    for entry in raw:
        token_id = entry.get('id') if isinstance(entry, dict) else None
        if not isinstance(token_id, int) or isinstance(token_id, bool) or token_id <= 0:
            raise ValueError('api.tokens: "id" must be a positive integer')
        if token_id in seen_ids:
            raise ValueError('api.tokens: duplicate id {}'.format(token_id))
        seen_ids.add(token_id)

        sha256 = str(entry.get('sha256', '')).lower()
        if not _SHA256_RE.match(sha256):
            raise ValueError('api.tokens: token {} needs "sha256" as 64 hex chars'.format(token_id))

        user_ids = _int_list_or_none(entry, 'user_ids')
        if user_ids is not None and any(u < MIN_USER_ID for u in user_ids):
            raise ValueError('api.tokens: token {} has user_ids below {}'.format(token_id, MIN_USER_ID))
        problems = _int_list_or_none(entry, 'problems')

        tokens.append(ApiToken(token_id, entry.get('name', ''), sha256, user_ids, problems))
    return tokens


def error_response(status, message, error_code=None):
    body = {'status': 'error', 'status_code': status, 'error': message}
    if error_code:
        body['error_code'] = error_code
    return Response(json_body=body, status=status)


def authenticate(request):
    """Returns (token, None) or (None, error response)."""
    header = request.headers.get('Authorization', '')
    scheme, _, secret = header.partition(' ')
    secret = secret.strip()
    if scheme.lower() != 'bearer' or not secret:
        return None, error_response(401, 'Bearer token is required')

    digest = hashlib.sha256(secret.encode('utf-8')).hexdigest()
    found = None
    # no early exit, so the response time doesn't depend on which token matched
    for token in parse_api_tokens(request.registry.settings):
        if compare_digest(digest, token.sha256):
            found = token
    if found is None:
        return None, error_response(401, 'Invalid token')
    return found, None
