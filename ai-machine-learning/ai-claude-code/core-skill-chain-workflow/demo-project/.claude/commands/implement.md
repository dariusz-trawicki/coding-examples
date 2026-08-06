---
description: "Implements the change phase by phase according to plan.md"
argument-hint: "[change name] [optional: phase number]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

# Implement — Implementation

Stage: **Implementation**. The developer stays in control — the agent
doesn't do everything at once.

## Arguments
`$ARGUMENTS` — change name, optionally followed by a specific phase number
(e.g. `lazy-load-search 2` = implement only Phase 2).

## Your task

1. **Load `context/<change>/plan.md`**. If it doesn't exist — stop and
   point to `/plan`.

2. **Determine which phase you're implementing.**
   - If a phase number was given — implement only that one.
   - If not — ask (directly in the chat) whether to implement all phases in
     a row, or stop after each one for approval.

3. **For each phase:**
   a. Implement the steps described in `plan.md` for this phase, following
      the project's conventions (`CLAUDE.md`, existing code style in
      neighboring files).
   b. Run the tests/linters appropriate for the changed files (check
      `package.json`/`Makefile`/CI config to use the right commands).
   c. Verify the "Phase verification" checklist from `plan.md`.
   d. If something during implementation **deviates from the plan** (e.g.
      the plan turned out to be off once it met the real code) —
      **stop and ask the user** instead of quietly improvising.
   e. Save a short phase summary to `context/<change>/implementation-log.md`
      (append, don't overwrite):
      ```markdown
      ## Phase <N> — <date/time>
      - Implemented: ...
      - Tests: <result>
      - Deviations from plan: <if any>
      ```
   f. If in "stop after each phase" mode — end your turn and wait for
      approval before moving on.

4. Once the last phase is implemented, update the `## Status` section in
   `change.md` → `Stage: IMPLEMENTED`.

5. Finish with:
   > Implementation complete (or: Phase N complete). Manual verification
   > steps: <list, if any>. Next step: `/review $ARGUMENTS`

## Rules
- Don't go beyond the scope defined in `plan.md` without asking — this is
  the most common cause of "spaghetti commits" and messy reviews.
- Small, reviewable steps > one giant commit.
- If the project's test infrastructure isn't obvious — ask instead of
  guessing the command.
