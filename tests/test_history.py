"""Test history.log writes JSONL records correctly."""
import json
import os
import tempfile
from pathlib import Path
from unittest import mock

from aid import history


def test_log_writes_jsonl_record():
    with tempfile.TemporaryDirectory() as tmp:
        with mock.patch.object(history, "HISTORY_DIR", Path(tmp)), \
             mock.patch.object(history, "HISTORY_FILE", Path(tmp) / "history.jsonl"):
            history.log("plan", "groceries, gym", "morning: groceries\nafternoon: gym")
            content = (Path(tmp) / "history.jsonl").read_text(encoding="utf-8")
    record = json.loads(content.strip())
    assert record["command"] == "plan"
    assert record["input"] == "groceries, gym"
    assert "morning" in record["output"]
    assert "ts" in record


def test_log_appends_multiple():
    with tempfile.TemporaryDirectory() as tmp:
        with mock.patch.object(history, "HISTORY_DIR", Path(tmp)), \
             mock.patch.object(history, "HISTORY_FILE", Path(tmp) / "history.jsonl"):
            history.log("translate", "halo", "hello")
            history.log("translate", "selamat", "good")
            content = (Path(tmp) / "history.jsonl").read_text(encoding="utf-8")
    lines = [json.loads(l) for l in content.strip().split("\n")]
    assert len(lines) == 2
    assert lines[0]["input"] == "halo"
    assert lines[1]["input"] == "selamat"
