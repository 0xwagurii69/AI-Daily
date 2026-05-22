"""Summarize a URL or piped stdin to 5 bullets."""
import sys
import re
import httpx

from ..config import load
from ..llm import chat
from ..history import log

SYS_PROMPT = """Summarize the user's text in EXACTLY 5 bullet points.
- Each bullet: one sentence, max 20 words.
- Keep proper nouns and numbers verbatim.
- No preamble, no summary heading, just bullets."""


def _fetch(url: str) -> str:
    with httpx.Client(timeout=20, follow_redirects=True,
                      headers={"User-Agent": "Mozilla/5.0 aid/0.1"}) as c:
        r = c.get(url)
        r.raise_for_status()
        html = r.text
    # Strip script/style/nav, keep text. Quick + dirty, deliberately no BS4 dep.
    html = re.sub(r"<(script|style|nav|footer|header)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:8000]  # cap input for token budget


def run(source: str):
    cfg = load()
    if source and (source.startswith("http://") or source.startswith("https://")):
        text = _fetch(source)
        label = source
    else:
        # Read from stdin if no URL given
        text = sys.stdin.read() if not sys.stdin.isatty() else source
        label = "<stdin>" if not sys.stdin.isatty() else source
    if not text.strip():
        print("usage: aid summarize <url>   OR   echo 'text' | aid summarize")
        return
    out = chat(cfg, SYS_PROMPT, text, temperature=0.3)
    print(out)
    log("summarize", label, out)
