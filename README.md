# AI-Daily

Small Python utilities powered by LLMs for everyday life. One CLI, several focused commands — journaling, planning, recipe ideas, quick translate, page summarizer.

## Why

I keep falling back to ChatGPT for the same five or six tiny tasks every day. Opening a browser, signing in, scrolling through a chat thread is too much friction for a 30-second question. `aid` puts each of those routines behind a one-line shell command and stores results locally so I can grep my own history.

## Install

```bash
git clone https://github.com/0xwagurii69/ai-daily.git
cd ai-daily
pip install -e .
cp examples/config.example.toml ~/.config/aid/config.toml
# edit api_key + base_url
```

Works with any OpenAI-compatible endpoint — official OpenAI, local llama.cpp server, OpenRouter, custom gateways.

## Commands

```bash
aid journal              # interactive daily journal, AI follow-up questions
aid plan "groceries, finish report, call mom, gym"   # natural-language → structured day plan
aid recipe "telur, mie instan, daun bawang"          # ingredients → recipe ideas
aid translate "selamat malam"                         # quick translate (auto-detect lang)
aid summarize https://example.com/long-article        # URL or piped text → 5-bullet summary
```

All runs write to `~/.aid/history.jsonl` so you can replay or grep what you asked.

## Config

`~/.config/aid/config.toml`:

```toml
[llm]
base_url = "https://api.openai.com/v1"
api_key  = "sk-..."
model    = "gpt-4o-mini"
timeout  = 30
```

## Why no big framework

Single dep stack: `httpx` + `tomli` + `click`. No LangChain, no agents, no vector DB. The whole thing fits in ~500 LOC because each command is a one-shot prompt + response.

## License

MIT
