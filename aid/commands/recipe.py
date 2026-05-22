"""Suggest 3 quick recipes from given ingredients."""
from ..config import load
from ..llm import chat
from ..history import log

SYS_PROMPT = """Suggest 3 quick recipes (under 30 minutes) using only ingredients
the user mentions, plus pantry staples (oil, salt, pepper, water).
Format each as:
- name (cook time)
  - 2-3 step instructions in one line each
Be concise. Use the user's language."""


def run(ingredients: str):
    if not ingredients.strip():
        print("usage: aid recipe \"egg, instant noodles, scallion\"")
        return
    cfg = load()
    out = chat(cfg, SYS_PROMPT, ingredients, temperature=0.7)
    print(out)
    log("recipe", ingredients, out)
