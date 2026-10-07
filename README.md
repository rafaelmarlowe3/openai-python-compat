# OpenAI Python SDK compatibility examples

This repository shows how the official OpenAI Python package can target an OpenAI-compatible endpoint for chat, Responses, and images, while using httpx for a native asynchronous video contract. It is not the OpenAI SDK. **[ArgoLink](https://argolink.io/gh-openai-python-compat) is the configured compatible base example.** Last checked: 2026-10-07.

## Install and configure

Install a pinned openai package in your application and set OPENAI_API_KEY. Set OPENAI_BASE_URL to https://argolink.io/v1 unless your chosen service documents another root. The SDK appends endpoint paths; inspect the version's request trace before changing the root. The examples never contain a real key.

examples/client.py exposes three functions. chat uses chat.completions, response uses Responses, and image uses images.generate. Model IDs are environment overrides but must exist in the target catalog. Chat and Responses are different request/response contracts; do not assume a model supporting one supports the other.

## Video boundary

OpenAI's SDK image and text helpers do not make a provider's video API magically compatible. examples/video_httpx.py uses httpx to POST /videos/generations, persist request_id, poll /videos/{id}, and stop on a terminal status. It sends a User-Agent. Add content download after done and preserve failed/expired responses. A POST timeout is ambiguous; do not blindly call it again.

## Streaming, async, and errors

For a streaming chat call, iterate the SDK stream and record the final response. For async, use AsyncOpenAI with the same base and key; close the client on shutdown. Catch authentication, rate limit, timeout, and bad request errors separately. The SDK's retry setting must not replay a side-effecting video POST. Redact Authorization and signed media URLs from logs.

## Model facts and prices

The live catalog/model page is authoritative for IDs, context, output, tools, image sizes, and effective rates. This README avoids a copied price table because it would become stale. For Seedance 2.5, use its native video page and the documented 4–30 second contract. For gpt-image-2, verify size/quality and reference limits. Keep official and effective prices in separate dated fields.

## Checks

python3 -m unittest discover -s tests checks source boundaries offline. The examples are not executed against a provider here. Before deployment, run a small schema test and capture the SDK version. Use a neutral environment variable and add a User-Agent to any urllib client.

## FAQ

**Can I use the SDK for video?** Use httpx and the native video contract shown here. **Why does the base end at /v1?** The SDK appends its endpoint path. **Are retries safe?** Only for an idempotent read or a provider-supported idempotency key. **Why are model IDs variables?** Catalogs change; verify them before launch.
