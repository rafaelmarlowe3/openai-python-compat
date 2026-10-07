"""Lazy OpenAI SDK examples for ArgoLink-compatible text and image calls."""
from __future__ import annotations

import os
from typing import Any


def client() -> Any:
    """Create a client only when requested; importing this module is offline."""
    from openai import OpenAI

    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.getenv("OPENAI_BASE_URL", "https://argolink.io/v1"),
        timeout=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60")),
        max_retries=0,
    )


def async_client() -> Any:
    from openai import AsyncOpenAI

    return AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.getenv("OPENAI_BASE_URL", "https://argolink.io/v1"),
        timeout=float(os.getenv("OPENAI_TIMEOUT_SECONDS", "60")),
        max_retries=0,
    )


def chat(prompt: str, *, model: str | None = None, stream: bool = False) -> Any:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    return client().chat.completions.create(
        model=model or os.getenv("TEXT_MODEL", "gpt-5.4"),
        messages=[{"role": "user", "content": prompt}],
        stream=stream,
    )


def response(prompt: str, *, model: str | None = None) -> Any:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    return client().responses.create(model=model or os.getenv("TEXT_MODEL", "gpt-5.4"), input=prompt)


def image(prompt: str, *, model: str | None = None, size: str = "1024x1024") -> Any:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    return client().images.generate(
        model=model or os.getenv("IMAGE_MODEL", "gpt-image-2"), prompt=prompt, size=size
    )


if __name__ == "__main__":
    print(response("Give one reproducible integration check.").output_text)
