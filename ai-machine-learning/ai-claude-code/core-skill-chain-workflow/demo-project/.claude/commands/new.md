---
description: "Initializes a new unit of change (change) in the workflow"
argument-hint: "[short change name, e.g. lazy-load-search]"
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# New — Environment Preparation

You are at the **Environment Preparation** stage for a new change in the
project.

## Arguments
Change name (slug): `$ARGUMENTS`

If no name was provided, propose a sensible slug based on the conversation
context (kebab-case, English, max 4-5 words) and confirm it with the user.

## Your task

1. **Check the project context**
   - Read `CLAUDE.md` (if it exists) — conventions, stack, project rules.
   - Check if the `context/` directory exists — if not, create it.
   - Check if `context/$ARGUMENTS/` already exists. If so — ask the user
     whether to continue the existing change or overwrite it.

2. **Ask clarifying questions** (max 3-5 questions, proportional to the
   complexity of the topic — don't overdo it) directly in the chat.
   **Wait for the user's reply in their next message before continuing.**
   - What is the business/technical goal of this change?
   - What is the scope (what IS and what is explicitly NOT included)?
   - Are there any hard constraints (deadline, backward compatibility,
     specific libraries to use/avoid)?
   - What is the expected level of test coverage?

3. **Create the change structure**
   ```
   context/$ARGUMENTS/
     change.md
   ```

4. **Fill in `change.md`** using this template:

   ```markdown
   # Change: <Change name>

   ## Status
   - Stage: NEW
   - Created: <date>

   ## Goal
   <1-3 sentences — why we are making this change>

   ## Scope
   ### In scope
   - ...

   ### Out of scope
   - ...

   ## Constraints and requirements
   - ...

   ## Acceptance criteria
   - [ ] ...
   - [ ] ...

   ## Notes from the initial conversation
   <raw answers from the user in step 2 — this is the source of truth for
   subsequent skills>
   ```

5. **Do not start research or implementation.** This skill ends once
   `change.md` is created. Finish by telling the user explicitly:
   > Change `$ARGUMENTS` has been initialized. Next step: `/research $ARGUMENTS`

## Rules
- Don't guess the business goal — if you don't know something, ask.
- Don't write code, tests, or a plan at this stage.
- `change.md` is the only artifact of this step and must be self-contained —
  the next skill (`research`) will read it without any additional context
  from this conversation.
