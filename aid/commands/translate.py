"""Quick translate — auto-detects source, defaults target = English."""
from ..config import load
from ..llm import chat
from ..history import log

SYS_PROMPT = """You are a precise translator.
- Auto-detect source language.
- Translate to English unless the input is already English (then translate to Indonesian).
- Output ONLY the translation. No quotes, no commentary."""


def run(text: str):
    if not text.strip():
        print("usage: aid translate \"text here\"")
        return
    cfg = load()
    out = chat(cfg, SYS_PROMPT, text, temperature=0.2)
    print(out)
    log("translate", text, out)
