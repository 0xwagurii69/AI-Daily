"""Thin OpenAI-compatible chat client."""
import json
import httpx

from .config import Config


def chat(cfg: Config, system: str, user: str, *, temperature: float = 0.7) -> str:
    """One-shot chat completion. Returns assistant message content."""
    payload = {
        "model": cfg.model,
        "temperature": temperature,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    headers = {
        "Authorization": f"Bearer {cfg.api_key}",
        "Content-Type": "application/json",
    }
    url = f"{cfg.base_url}/chat/completions"
    with httpx.Client(timeout=cfg.timeout) as client:
        r = client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
    return data["choices"][0]["message"]["content"].strip()
