---
description: "Builds a mental map of the change based on the repository (research.md)"
argument-hint: "[change name]"
allowed-tools: ["Read", "Grep", "Glob", "Bash", "Task"]
---

# Research — Problem Assessment

Stage: **Problem assessment**. Goal: a deep understanding of the system
before a single line of plan or code is written.

## Arguments
Change name: `$ARGUMENTS`

## Your task

1. **Load context**
   - Read `context/$ARGUMENTS/change.md`. If it doesn't exist — stop and
     tell the user to run `/new $ARGUMENTS` first.
   - Read `CLAUDE.md` and other convention files (`.editorconfig`,
     `README.md`, existing ADRs, if any).

2. **Break the research into sub-problems and delegate to sub-agents**
   If the scope of the change touches more than one area (e.g. frontend +
   backend + storage + CI), use the `Task` tool to spin up **separate
   sub-agents** for each area, e.g.:
   - sub-agent A: "Investigate how X currently works in `src/...`, return a
     concise report (max 1 page): key files, data flow, extension points."
   - sub-agent B: "Investigate how Y is tested, what the existing testing
     conventions are."

   Each sub-agent gets its **own context window** and returns a short
   report — don't flood the main context with raw grep/read output.

3. **Build `research.md`** using this template:

   ```markdown
   # Research: <Change name>

   ## How it works today
   <description of the current behavior/architecture, with references to
   files: `path/to/file.ts:42`>

   ## Why the current behavior exists
   <root cause — historical decision, technical constraint, tech debt>

   ## Key files and modules
   - `path/...` — role in the system
   - `path/...` — role in the system

   ## Risks and pitfalls
   - <what could easily break, hidden dependencies, missing tests in this area>

   ## Open questions for the planning phase
   - <questions the research did not conclusively answer>

   ## Recommended direction (optional)
   <if an obvious direction emerges during research — note it, but don't
   decide for the user>
   ```

4. **Save the file** as `context/$ARGUMENTS/research.md`.

5. Update the `## Status` section in `change.md` → `Stage: RESEARCH DONE`.

6. Finish with:
   > Research complete. Next step: `/plan $ARGUMENTS`

## Rules
- Don't propose a specific implementation plan yet — that's the `plan`
  skill's job. Research should ANSWER "how is it now and why", not
  "what do we do next".
- Cite specific file paths and lines, not generalities.
- If the repo is large, always delegate to sub-agents instead of reading
  everything sequentially in the main thread.
