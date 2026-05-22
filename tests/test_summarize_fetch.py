"""Test summarize._fetch strips HTML tags and caps length."""
import re
from unittest import mock

from aid.commands import summarize


def test_fetch_strips_tags(monkeypatch):
    fake_html = "<html><head><script>alert(1)</script></head><body><p>Hello world</p><nav>nav</nav></body></html>"

    class FakeResp:
        text = fake_html
        def raise_for_status(self): pass

    class FakeClient:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def get(self, url): return FakeResp()

    monkeypatch.setattr(summarize.httpx, "Client", FakeClient)
    out = summarize._fetch("https://example.com")
    assert "<" not in out
    assert "alert" not in out
    assert "nav" not in out
    assert "Hello world" in out


def test_fetch_caps_length(monkeypatch):
    big_text = "<p>" + ("x" * 50_000) + "</p>"

    class FakeResp:
        text = big_text
        def raise_for_status(self): pass

    class FakeClient:
        def __init__(self, *a, **kw): pass
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def get(self, url): return FakeResp()

    monkeypatch.setattr(summarize.httpx, "Client", FakeClient)
    out = summarize._fetch("https://example.com")
    assert len(out) <= 8000
