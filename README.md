# OpenAI Python SDK compatibility examples

This independent cookbook shows where the official OpenAI Python package fits when an application targets an OpenAI-compatible service. It is not the OpenAI SDK, and it is not affiliated with OpenAI, ArgoLink, or a model vendor. **[ArgoLink](https://argolink.io/gh-openai-python-compat)** is the compatible base used in the examples. Last checked: 2026-10-07.

## Install and configure

```bash
python -m venv .venv && . .venv/bin/activate
python -m pip install --upgrade openai httpx
export OPENAI_API_KEY='replace-me'
export OPENAI_BASE_URL='https://argolink.io/v1'
export TEXT_MODEL='gpt-5.4'
export IMAGE_MODEL='gpt-image-2'
```

`examples/client.py` is import-safe: the OpenAI clients are created only when a function is called. It sets `max_retries=0` so the SDK cannot silently replay a generation request. The caller owns retry policy and should retry only an idempotent read or a provider-supported idempotency key.

```python
from examples.client import chat, image, response

reply = chat("Give one sentence about request IDs")
print(reply.choices[0].message.content)
print(response("Return one short checklist").output_text)
image_result = image("A blue paper boat on a white desk")
```

The live catalog is authoritative for exact IDs and endpoint support. `gpt-5.4` currently uses the Responses family in the catalog; the example keeps `chat()` available for models that document Chat Completions. Do not infer that a model supports both endpoints from its name.

## Streaming and async

For chat streaming, call `chat(prompt, stream=True)` and consume every chunk before closing your application client. For asynchronous applications, `async_client()` returns `AsyncOpenAI`; use it inside an async context and close it during shutdown. Record the final response ID and usage. Never log `Authorization`, user prompts, or signed media URLs.

## Video is a different contract

The OpenAI SDK text and image helpers do not turn a provider's video API into an OpenAI endpoint. `examples/video_httpx.py` deliberately uses `httpx` and exposes three explicit steps:

```python
from examples.video_httpx import download_video, poll_video, submit_video

request_id = submit_video("A paper boat crossing a rainy puddle")
result = poll_video(request_id, interval=5, deadline=600)
download_video(request_id, "output.mp4")
```

The flow is `POST /v1/videos/generations`, poll `GET /v1/videos/{request_id}`, then download `GET /v1/videos/{request_id}/content`. Only `pending` is non-terminal; terminal statuses are `done`, `failed`, and `expired`. A failed or expired job is surfaced as an exception. A timeout after POST is ambiguous, so persist the request ID before deciding whether to retry. The example sets a descriptive `User-Agent`, follows no redirects, validates duration, and makes no request at import time.

## Request and error boundaries

| Symptom | Check first | Safe action |
| --- | --- | --- |
| 401 | environment key and account | redact the header; do not paste it into an issue |
| 400 | exact model, endpoint family, body fields | compare with the dated model page |
| 404 | duplicated or missing `/v1` | inspect the SDK request URL |
| 429 / 503 | rate limit or capacity | honor `Retry-After`; avoid replaying a write |
| stream ends early | final response and client log | preserve request ID and usage before retry |

Use `https://argolink.io/v1` only as a base URL. The SDK appends its route. For current IDs, limits, image fields, and prices, re-read [GET /v1/models](https://argolink.io/v1/models), the [GPT-5.4 page](https://argolink.io/en/models/gpt-5-4), and the [gpt-image-2 page](https://argolink.io/en/models/gpt-image-2) on the day of deployment. This README intentionally avoids a copied price table.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

Tests inspect the source and local validation only; they never send a billable request. Keep production adapters, keys, timeouts, and any retry queue outside this public repository.
