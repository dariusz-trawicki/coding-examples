---
description: "Creates an implementation plan (plan.md + plan-brief.md) in an interactive dialogue"
argument-hint: "[change name]"
allowed-tools: ["Read", "Write", "Grep", "Glob"]
---

# Plan — Preparation

Stage: **Plan preparation**. Here the agent takes on a Socratic role — not
just planning, but **challenging and asking questions**.

## Arguments
Change name: `$ARGUMENTS`

## Your task

1. **Load `change.md` and `research.md`** from `context/$ARGUMENTS/`.
   If `research.md` doesn't exist, stop and ask the user to run
   `/research $ARGUMENTS` first.

2. **Assess the complexity of the change** (low / medium / high) based on:
   - the number of affected modules/layers,
   - risks listed in `research.md`,
   - whether the change touches public API / contracts / production data.

3. **Ask questions matched to the complexity**, directly in the chat, and
   **wait for the user's reply before writing plan.md**:
   - **Low complexity** → 3-5 questions, mostly confirming direction.
   - **Medium/High complexity** → more questions, including trade-offs
     between specific implementation options (present options with their
     pros/cons, let the user choose).

   Example question categories:
   - Choice of technical approach (if there is more than one sensible option).
   - Ordering of phases — what can safely be shipped separately.
   - Testing strategy (unit / integration / e2e / manual steps).
   - Handling of edge cases identified in research.md.

   **Don't ask questions just for the sake of asking.** If the answer is
   obvious from `change.md`/`research.md`, don't ask again.

4. **Write `plan.md`** (detailed, for the agent, roughly 150-300 lines):

   ```markdown
   # Plan: <Change name>

   ## Context
   <1 paragraph — reference to change.md and research.md, without repeating
   their content>

   ## Phase 1: <name>
   ### Phase goal
   ...
   ### Steps
   1. ...
   2. ...
   ### Files to change
   - `path/...`
   ### Phase verification
   - [ ] tests: ...
   - [ ] manual verification: ...

   ## Phase 2: <name>
   (same structure)

   ## Risks and mitigations
   - ...

   ## Definition of Done
   - [ ] all acceptance criteria from change.md are met
   - [ ] tests pass
   - [ ] no regression in <specific areas>
   ```

5. **Write `plan-brief.md`** (concise, for the human, <100 lines):

   ```markdown
   # Plan (brief): <Change name>

   ## What we're doing
   <2-3 sentences>

   ## Phases
   1. <phase name — 1 sentence>
   2. <phase name — 1 sentence>

   ## Key decisions made during planning
   - <decision> — why

   ## What to watch for during review
   - <the riskiest part>
   ```

6. Update the `## Status` section in `change.md` → `Stage: PLANNED`.

7. Finish with:
   > Plan ready (`plan.md` + `plan-brief.md`). Review `plan-brief.md` before
   > starting. Next step: `/implement $ARGUMENTS`

## Rules
- The level of user engagement should be proportional to actual complexity —
  don't overwhelm a simple change with questions.
- `plan.md` and `plan-brief.md` have two different audiences: agent vs.
  human. Don't copy content 1:1 between them.
- Don't start implementation at this stage, even if the plan seems obvious.
