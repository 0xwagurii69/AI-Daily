"""Load aid config from ~/.config/aid/config.toml."""
import os
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib

CONFIG_PATH = Path(os.path.expanduser("~/.config/aid/config.toml"))


class Config:
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout


def load() -> Config:
    if not CONFIG_PATH.exists():
        sys.exit(
            f"config not found: {CONFIG_PATH}\n"
            "copy examples/config.example.toml there and fill in api_key + base_url"
        )
    with open(CONFIG_PATH, "rb") as f:
        data = tomllib.load(f)
    llm = data.get("llm", {})
    missing = [k for k in ("base_url", "api_key", "model") if not llm.get(k)]
    if missing:
        sys.exit(f"config missing keys under [llm]: {missing}")
    return Config(
        base_url=llm["base_url"],
        api_key=llm["api_key"],
        model=llm["model"],
        timeout=int(llm.get("timeout", 30)),
    )
