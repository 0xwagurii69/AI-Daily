"""Append every aid run to ~/.aid/history.jsonl for personal grep-ability."""
import json
import os
import time
from pathlib import Path

HISTORY_DIR = Path(os.path.expanduser("~/.aid"))
HISTORY_FILE = HISTORY_DIR / "history.jsonl"


def log(command: str, input_: str, output: str) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "command": command,
        "input": input_,
        "output": output,
    }
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
