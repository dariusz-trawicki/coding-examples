# Deep Agent Demo

A minimal, complete example of the **deep agent** architecture — planning,
a filesystem for offloading context, and isolated subagents — using the
Anthropic API and Tavily for web search.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- An Anthropic API key: https://console.anthropic.com/settings/keys
- A Tavily API key (free tier): https://tavily.com

## Run it

```bash
cp .env.example .env   # then edit .env with your real keys
uv sync
uv run main.py
```

## Demo goal

The `if __name__ == "__main__":` block runs this goal by default:

> Search the web for recent approaches to deep agent architecture, then write a short example in Python illustrating one of them.

It's deliberately "meaty" — it exercises all four tools in one run: planning (`write_todos`), research (`tavily_search`), delegation (`delegate_to_subagent`), and reading back a result (`read_file`). Edit the `goal` variable in `main.py` to try your own.

## Output files

Long results (subagent output, research notes, code) are written as real files under `./workspace/`. After a run, `main.py` lists what landed there, e.g.:

```
Files saved to ./workspace/:
  - workspace/subagent_coder.txt
  - workspace/subagent_researcher.txt
```

## Architecture

| Component | Role |
|---|---|
| `write_todos` | Orchestrator plans before acting |
| `VirtualFileSystem` | Long results live outside the conversation |
| `delegate_to_subagent` | Subtasks run in isolated, fresh conversations |
| `tavily_search` | Concise, agent-ready web search results |

Orchestrator runs on a stronger model (`claude-sonnet-4-6`); subagents run
on a faster, cheaper one (`claude-haiku-4-5-20251001`).
