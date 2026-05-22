"""Turn a comma-separated brain dump into a structured day plan."""
from ..config import load
from ..llm import chat
from ..history import log

SYS_PROMPT = """You turn the user's comma-separated tasks into a realistic day plan.
- Group by morning / afternoon / evening based on energy and dependencies.
- Each task gets ONE actionable verb + estimated minutes.
- Skip filler words. Output as plain markdown, no preamble.
- 8 lines maximum total."""


def run(tasks: str):
    if not tasks.strip():
        print("usage: aid plan \"task1, task2, task3\"")
        return
    cfg = load()
    out = chat(cfg, SYS_PROMPT, tasks, temperature=0.5)
    print(out)
    log("plan", tasks, out)
