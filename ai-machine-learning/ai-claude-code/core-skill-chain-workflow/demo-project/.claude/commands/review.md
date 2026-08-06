---
description: "Verifies the implementation against plan.md — scope compliance, not just code correctness"
argument-hint: "[change name]"
allowed-tools: ["Read", "Grep", "Glob", "Bash"]
---

# Review — Quality Assessment

Stage: **Quality assessment**. This is NOT a generic code review — it's a
verification of **compliance between the implementation and the plan**,
plus overall quality.

> 💡 Tip: if possible, run this step with a different model than the one
> that wrote the code (e.g. if Sonnet wrote the code, have a different
> model do the review). Different models catch each other's mistakes more
> effectively than the same model reviewing itself.

## Arguments
Change name: `$ARGUMENTS`

## Your task

1. **Load** `change.md`, `plan.md`, `implementation-log.md`, and the actual
   diff of changes (`git diff` against the base branch or the last commit
   before the change).

2. **Check three layers:**

   ### A. Scope compliance
   - Was exactly what's in `plan.md` implemented?
   - Is there any scope creep (code outside the plan)?
   - Are all "Definition of Done" items from `plan.md` met?
   - Are all acceptance criteria from `change.md` met?

   ### B. Code quality
   - Compliance with project conventions (`CLAUDE.md`, style of
     neighboring files).
   - Readability, no dead code, no leftover `TODO`/`console.log`/commented
     out code.
   - Handling of edge cases identified in `research.md`.

   ### C. Tests and change safety
   - Do the tests actually cover the new logic (not just "pass").
   - Is there a risk of regression in areas not directly related to the
     change.

3. **Build `review.md`**:

   ```markdown
   # Review: <Change name>

   ## Scope compliance
   - [ ] / [x] <item> — comment

   ## Issues found
   ### 🔴 Blocking
   - ...

   ### 🟡 Worth considering
   - ...

   ### 🟢 Nice-to-have
   - ...

   ## Verdict
   READY / NEEDS FIXES / NEEDS DISCUSSION
   ```

4. **For each issue found** — ask the user directly in the chat to
   interactively decide: fix now / accept as tech debt / skip. Don't fix
   things automatically without confirmation — the developer decides what
   is good enough.

5. Update the `## Status` section in `change.md` → `Stage: REVIEWED` (or
   `NEEDS FIXES` if there are blockers).

6. Finish with:
   > Review complete. Verdict: <READY/NEEDS FIXES>. If READY →
   > `/archive $ARGUMENTS`. If NEEDS FIXES → go back to
   > `/implement $ARGUMENTS` after fixes.

## Rules
- Priority: compliance with the plan > code aesthetics. Beautiful code that
  does something other than what was planned is not a success at this stage.
- Don't close a review with blockers without the user's explicit consent.
