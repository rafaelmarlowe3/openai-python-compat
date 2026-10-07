"""Small, explicit client for ArgoLink's asynchronous video contract.

No request is made at import time. A caller must deliberately invoke submit_video.
"""
from __future__ import annotations

import os
import time
from typing import Any

import httpx

BASE_URL = os.getenv("OPENAI_BASE_URL", "https://argolink.io/v1").rstrip("/")
USER_AGENT = "openai-python-compat/1.0"
TERMINAL = {"done", "failed", "expired"}


def _headers() -> dict[str, str]:
    return {
        "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"],
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }


def submit_video(prompt: str, *, model: str = "seedance-2.5", duration: int = 5, resolution: str = "720p", aspect_ratio: str = "16:9") -> str:
    if not prompt.strip():
        raise ValueError("prompt must not be empty")
    if duration < 4 or duration > 30:
        raise ValueError("Seedance 2.5 duration must be 4-30 seconds")
    payload = {"model": model, "prompt": prompt, "duration": duration, "resolution": resolution, "aspect_ratio": aspect_ratio}
    with httpx.Client(base_url=BASE_URL, timeout=90.0, headers=_headers(), follow_redirects=False) as http:
        response = http.post("/videos/generations", json=payload)
        response.raise_for_status()
        request_id = response.json().get("request_id")
        if not isinstance(request_id, str) or not request_id:
            raise RuntimeError("generation response did not contain request_id")
        return request_id


def poll_video(request_id: str, *, interval: float = 5.0, deadline: float = 600.0) -> dict[str, Any]:
    if not request_id.strip():
        raise ValueError("request_id must not be empty")
    if interval <= 0 or deadline <= 0:
        raise ValueError("interval and deadline must be positive")
    end = time.monotonic() + deadline
    with httpx.Client(base_url=BASE_URL, timeout=30.0, headers=_headers(), follow_redirects=False) as http:
        while True:
            response = http.get("/videos/" + request_id)
            response.raise_for_status()
            result = response.json()
            status = result.get("status")
            if status in TERMINAL:
                if status != "done":
                    raise RuntimeError(f"video job ended with status={status}")
                return result
            if status != "pending":
                raise RuntimeError(f"unexpected video status={status!r}")
            if time.monotonic() + interval > end:
                raise TimeoutError("video job did not finish before deadline")
            time.sleep(interval)


def download_video(request_id: str, destination: str) -> None:
    if not request_id.strip() or not destination:
        raise ValueError("request_id and destination are required")
    with httpx.Client(base_url=BASE_URL, timeout=90.0, headers=_headers(), follow_redirects=False) as http:
        response = http.get("/videos/" + request_id + "/content")
        response.raise_for_status()
        with open(destination, "wb") as handle:
            handle.write(response.content)
