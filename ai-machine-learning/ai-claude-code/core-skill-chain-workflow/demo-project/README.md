# Demo Project — Workflow for Claude Code

A minimal sandbox project to try out a repeatable Core Skill Chain
workflow for Claude Code: six slash commands that carry a change through
its full lifecycle, each consuming the previous step's artifact and
producing its own.

## Structure

```
demo-project/
├── calc.py            ← a tiny toy app: add(), subtract()
├── .claude/commands/   ← the six workflow commands
├── context/            ← active changes live here
└── archive/            ← closed changes end up here
```

## Commands

```
/new         → Environment preparation   (change.md)
/research    → Problem assessment        (research.md)
/plan        → Preparation               (plan.md + plan-brief.md)
/implement   → Implementation            (code + implementation-log.md)
/review      → Quality assessment        (review.md)
/archive     → Cleanup                   (moved to archive/)
```

## Try it: add multiply() and divide()

1. Unzip and enter the folder:
   ```bash
   cd demo-project
   claude
   ```

2. Run through the chain:
   ```
   /new multiply-divide
   /research multiply-divide
   /plan multiply-divide
   /implement multiply-divide
   /review multiply-divide
   /archive multiply-divide
   ```

3. Whenever Claude asks you clarifying questions, just answer in your next
   message — it will wait and then continue automatically.

By the end, `calc.py` should have four working functions (`add`,
`subtract`, `multiply`, `divide`, with `divide` raising a `ValueError` on
division by zero), and you'll have a full paper trail in
`archive/multiply-divide-<date>/` explaining every decision along the way.

## Notes

- Each change gets its own isolated folder under `context/` — no global
  state file. If a direction turns out wrong, just delete the folder.
- `context/` should only ever contain active changes; finished ones move
  to `archive/` to keep the context small for future sessions.
- If your context window fills up mid-session, run `/compact` or
  `/clear` — the workflow's state lives in files, not in the chat history,
  so nothing is lost.
