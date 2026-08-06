---
description: "Closes the change — moves artifacts to archive/, cleans up context"
argument-hint: "[change name]"
allowed-tools: ["Read", "Bash", "Write"]
---

# Archive — Cleanup

Stage: **Cleanup**. The last step of the chain — keeping `context/` tidy
and building a searchable knowledge history of the project.

## Arguments
Change name: `$ARGUMENTS`

## Your task

1. **Check the status** in `context/$ARGUMENTS/change.md`. If the status is
   not `REVIEWED` (verdict READY), warn the user and ask for confirmation
   that they still want to archive (e.g. a change deliberately abandoned).

2. **Build a final summary of the change** — add a section at the top of
   `change.md`:

   ```markdown
   ## Final summary
   - Archived: <date>
   - Final review verdict: <READY / abandoned>
   - Key takeaways / lessons: <if there's anything worth remembering for
     the future>
   ```

3. **Move the entire change folder**:
   ```bash
   mkdir -p archive
   mv context/$ARGUMENTS archive/$ARGUMENTS-$(date +%Y%m%d)
   ```

4. **If recurring problems came up while working on the change** (linter
   errors, broken conventions, misunderstandings about the stack) —
   propose adding a short note to `CLAUDE.md` or a dedicated
   `context/LESSONS.md` file (if the project uses one), so future agent
   sessions don't repeat the same mistake. Ask the user for permission
   before editing `CLAUDE.md`.

5. Confirm to the user:
   > Change `$ARGUMENTS` archived in `archive/`. The `context/` directory
   > now contains only changes in progress.

## Rules
- `context/` should always contain only active changes — this is a
  deliberate constraint so the context passed to the agent in future
  sessions doesn't grow indefinitely.
- `archive/` is not a trash bin — it's a searchable history of decisions.
  Don't delete files from it without an explicit request from the user.
