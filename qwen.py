"""Minimal helpers for the self-hosted Qwen API."""

from __future__ import annotations

import base64
import mimetypes
import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def _env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def _config() -> tuple[str, str, str]:
    url = _env("QWEN_API_URL").rstrip("/")
    key = _env("QWEN_API_KEY")
    model = _env("QWEN_MODEL")
    return url, key, model


def _headers(api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _file_to_data_url(path: str | Path) -> str:
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    mime, _ = mimetypes.guess_type(str(path))
    if mime is None:
        mime = "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _build_content(
    prompt: str,
    image: str | Path | None = None,
    video: str | Path | None = None,
) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    if image is not None:
        content.append(
            {
                "type": "image_url",
                "image_url": {"url": _file_to_data_url(image)},
            }
        )
    if video is not None:
        content.append(
            {
                "type": "video_url",
                "video_url": {"url": _file_to_data_url(video)},
            }
        )
    return content


def chat(
    prompt: str,
    image: str | Path | None = None,
    video: str | Path | None = None,
    max_tokens: int = 512,
) -> str:
    """Send a multimodal chat completion request and return the reply text."""
    base_url, api_key, model = _config()
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": _build_content(prompt, image=image, video=video),
            }
        ],
        "max_tokens": max_tokens,
    }
    response = requests.post(
        f"{base_url}/chat/completions",
        headers=_headers(api_key),
        json=payload,
        timeout=300,
    )
    if not response.ok:
        raise RuntimeError(
            f"chat/completions failed ({response.status_code}): {response.text[:500]}"
        )
    data = response.json()
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected chat response: {data}") from exc
