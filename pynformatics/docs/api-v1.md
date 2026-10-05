# API v1: submit as a user and read run status

Both endpoints take `Authorization: Bearer <token>`. A token is configured in
the `api.tokens` setting (`config.secret`):

```json
"api.tokens": [
  {"id": 7, "name": "bot1", "sha256": "<sha256 hex of the token>",
   "user_ids": null, "problems": null}
]
```

- `user_ids` / `problems`: allowlists, `null` means any. Both keys are required.
- User ids of 2 or lower are always rejected.
- Runs are stamped with the token's own context (`10_000_000 + id`), and the
  status endpoint only shows runs of that context.

Make a token and its hash:

```bash
TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
printf %s "$TOKEN" | shasum -a 256
```

## Submit

`POST /api/v1/problem/{problem_id}/submit`, multipart form:

| field     | description                                  |
|-----------|----------------------------------------------|
| `user_id` | user to submit as                            |
| `lang_id` | language id                                  |
| `file`    | the source                                   |

```bash
curl -X POST https://informatics.msk.ru/api/v1/problem/42/submit \
  -H "Authorization: Bearer $TOKEN" \
  -F user_id=101 \
  -F lang_id=27 \
  -F file=@solution.py
```

```json
{"run_id": 9}
```

## Run status

`GET /api/v1/run/{run_id}/status`

```bash
curl https://informatics.msk.ru/api/v1/run/9/status \
  -H "Authorization: Bearer $TOKEN"
```

```json
{"ejudge_status": 377, "ejudge_score": null, "ejudge_test_num": null}
```

`ejudge_score` and `ejudge_test_num` are `null` until the run is tested.
`ejudge_status` is the ejudge verdict code; 377 means the run is in the queue.
Poll until it changes.

## Errors

Errors are JSON with the matching HTTP status:

```json
{"status": "error", "status_code": 403, "error": "Token is not allowed to submit as this user"}
```

| status | meaning |
|--------|---------|
| 400 | missing or invalid `user_id`, `lang_id` or `file`; rmatics rejections such as a duplicate of the previous submission |
| 401 | missing, malformed or unknown token |
| 403 | user or problem is not allowed for the token |
| 404 | run not found, or it was not created by this token |
| 502 | rmatics is unavailable |
