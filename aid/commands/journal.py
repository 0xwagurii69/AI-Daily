"""Interactive daily journal — AI asks follow-up questions."""
import sys

from ..config import load
from ..llm import chat
from ..history import log

SYS_PROMPT = """You are a thoughtful daily-journal partner.
The user shares a brief reflection about their day. You ask ONE short, specific
follow-up question that would help them think deeper or notice a pattern.
Keep your reply under 25 words. No coaching cliches, no toxic positivity."""


def run():
    print("aid journal — write a sentence or paragraph, blank line to finish.")
    print("(empty input = quit)\n")
    lines = []
    while True:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not line.strip() and not lines:
            return
        if not line.strip():
            break
        lines.append(line)
    entry = "\n".join(lines)

    cfg = load()
    follow_up = chat(cfg, SYS_PROMPT, entry, temperature=0.8)
    print(f"\n💭 {follow_up}\n")
    log("journal", entry, follow_up)
