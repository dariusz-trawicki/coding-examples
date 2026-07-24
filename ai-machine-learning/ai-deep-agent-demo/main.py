"""
Deep Agent Demo
===============

A minimal, working example of the "deep agent" architecture behind tools
like Claude Code, Deep Research, and Manus:

    1. Planning        -> agent writes a todo list before acting
    2. Filesystem       -> long intermediate results are stored outside
                           the conversation, not inlined into context
    3. Subagents        -> subtasks run in isolated, fresh conversations
                           instead of bloating the orchestrator's context

Uses the Anthropic API (orchestration + subagents) and Tavily
(web search built for LLM agents - concise results, not raw HTML).

Run with uv:
    cp .env.example .env   # add your API keys
    uv sync
    uv run main.py
"""

import os
import requests
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# Two models for two roles: a stronger model for planning/orchestration,
# a fast/cheap one for narrow, well-defined subagent tasks.
ORCHESTRATOR_MODEL = "claude-sonnet-4-6"
SUBAGENT_MODEL = "claude-haiku-4-5-20251001"


# ---------------------------------------------------------------------------
# 1. Filesystem
# ---------------------------------------------------------------------------
# Intermediate results are written to ./workspace/
WORKSPACE_DIR = "workspace"


class VirtualFileSystem:
    def __init__(self, root: str = WORKSPACE_DIR):
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def _path(self, path: str) -> str:
        # Keep everything inside the workspace directory - strip any
        # leading slashes so an odd `path` can't escape it.
        return os.path.join(self.root, path.lstrip("/"))

    def write(self, path: str, content: str) -> str:
        full_path = self._path(path)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Saved '{path}' ({len(content)} chars) to {full_path}"

    def read(self, path: str) -> str:
        full_path = self._path(path)
        if not os.path.exists(full_path):
            return f"ERROR: file '{path}' not found."
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()


vfs = VirtualFileSystem()


# ---------------------------------------------------------------------------
# 2. Web search tool (Tavily)
# ---------------------------------------------------------------------------
def tavily_search(query: str) -> str:
    """Tavily is built for LLM agents: it returns short, ready-to-use
    snippets instead of raw HTML, keeping the model's context clean."""
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": os.environ["TAVILY_API_KEY"],
            "query": query,
            "max_results": 5,
            "search_depth": "basic",
        },
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("results", [])
    lines = [
        f"- {r.get('title', '(no title)')}: {r.get('content', '')[:200]}... ({r.get('url', '')})"
        for r in results
    ]
    return "\n".join(lines) if lines else "No results found."


# ---------------------------------------------------------------------------
# 3. Subagent
# ---------------------------------------------------------------------------
def delegate_to_subagent(subagent_role: str, task: str) -> str:
    """Spins up a fresh, isolated conversation - the subagent sees only
    its own task, not the orchestrator's history. The full result is
    saved to the filesystem; the orchestrator gets back a short preview."""
    print(f"    [subagent:{subagent_role}] task: {task}")

    response = client.messages.create(
        model=SUBAGENT_MODEL,
        max_tokens=1024,
        system=(
            f"You are a specialized '{subagent_role}' subagent. "
            f"Complete ONLY the assigned task, concisely and directly."
        ),
        messages=[{"role": "user", "content": task}],
    )
    full_result = "".join(b.text for b in response.content if b.type == "text")

    file_path = f"subagent_{subagent_role}.txt"
    vfs.write(file_path, full_result)

    preview = full_result[:150].replace("\n", " ")
    return (
        f"Subagent '{subagent_role}' finished. Full result saved to "
        f"'{file_path}'. Preview: {preview}..."
    )


# ---------------------------------------------------------------------------
# Tool definitions for Claude
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "name": "write_todos",
        "description": "Write or update the task plan. Call this first for complex goals.",
        "input_schema": {
            "type": "object",
            "properties": {"todos": {"type": "array", "items": {"type": "string"}}},
            "required": ["todos"],
        },
    },
    {
        "name": "tavily_search",
        "description": "Search the web for current information.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "delegate_to_subagent",
        "description": (
            "Delegate a narrow, well-defined subtask to an isolated subagent "
            "(e.g. 'researcher', 'coder') instead of doing it inline."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "subagent_role": {"type": "string"},
                "task": {"type": "string"},
            },
            "required": ["subagent_role", "task"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the full content of a file from the filesystem.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
]

# Maps tool name -> the Python function that actually runs it.
DISPATCH = {
    "write_todos": lambda i: "Plan saved:\n" + "\n".join(f"  - {t}" for t in i["todos"]),
    "tavily_search": lambda i: tavily_search(i["query"]),
    "delegate_to_subagent": lambda i: delegate_to_subagent(i["subagent_role"], i["task"]),
    "read_file": lambda i: vfs.read(i["path"]),
}

ORCHESTRATOR_SYSTEM_PROMPT = """\
You are the orchestrator in a "deep agent" architecture. For complex tasks:

1. Start by writing a plan with write_todos.
2. Use tavily_search for anything requiring current information.
3. Delegate larger subtasks (research, code, long writing) to
   delegate_to_subagent instead of doing them inline.
4. Use read_file if you need the full detail behind a subagent's summary.
5. Finish with a concise, direct summary for the user. If a subagent
   produced code, quote the FULL code you retrieved via read_file - do
   not paraphrase or truncate it.
"""


# ---------------------------------------------------------------------------
# Orchestrator loop
# ---------------------------------------------------------------------------
def run_deep_agent(user_goal: str) -> str:
    messages = [{"role": "user", "content": user_goal}]

    while True:
        response = client.messages.create(
            model=ORCHESTRATOR_MODEL,
            max_tokens=4096,  # needs room for full code/text the agent quotes back
            system=ORCHESTRATOR_SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "max_tokens":
            # The response was cut off mid-generation, not finished on
            # purpose. Returning it as-is would silently hand back a
            # truncated answer (e.g. code cut in half). Surface this
            # clearly instead of pretending it's a real result.
            partial = "".join(b.text for b in response.content if b.type == "text")
            return (
                "[WARNING] Response was truncated at the max_tokens limit "
                f"before finishing.\nPartial output:\n{partial}"
            )

        if response.stop_reason != "tool_use":
            return "".join(b.text for b in response.content if b.type == "text")

        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"  [tool] {block.name}({block.input})")
            output = DISPATCH[block.name](block.input)
            tool_results.append(
                {"type": "tool_result", "tool_use_id": block.id, "content": output}
            )
        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    goal = (
        "Search the web for recent approaches to deep agent architecture, "
        "then write a short example in Python illustrating one of them."
    )
    print(f"GOAL: {goal}\n")
    print(run_deep_agent(goal))

    print(f"\nFiles saved to ./{WORKSPACE_DIR}/:")
    for name in sorted(os.listdir(WORKSPACE_DIR)):
        print(f"  - {WORKSPACE_DIR}/{name}")
