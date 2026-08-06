# Core Skill Chain — Workflow for Claude Code

A repeatable system for working with Claude Code on production codebases,
built as six custom slash commands. Each command handles one stage of a
change's lifecycle, consuming the previous stage's artifact and producing
its own — so the workflow stays consistent no matter who runs it, or which
model is behind the wheel that day.

## The problem this solves

One-shot prompting works fine for toy scripts and falls apart on real
projects. Without a workflow, common failure modes show up:

- **During preparation** — the agent skips business rules it doesn't know
  about, pulls context from the wrong places, and makes decisions without
  enough information from the developer.
- **During implementation** — code drifts from project conventions, there's
  no way to pause or steer mid-task, and different team members get wildly
  different results from the same prompt.
- **During integration** — messy commit history, thousands of undocumented
  lines dropped into a single review, reviewers unable to meaningfully
  evaluate the change.
- **No learning between sessions** — the agent is never taught how the team
  actually works. Every new session starts from zero, and the same problems
  resurface again and again.

## The idea: a chain of artifacts, not a single prompt

Building software is more than writing code — it's a sequence of related
stages: preparing the environment, whiteboarding an approach, implementing
in reviewable chunks, verifying quality, and leaving a documentation trail.
Core Skill Chain turns each of those stages into its own command, and each
command's output becomes the next command's input.

```
new         → Environment preparation   → change.md
research    → Problem assessment        → research.md
plan        → Preparation               → plan.md + plan-brief.md
implement   → Implementation            → code + implementation-log.md
review      → Quality assessment        → review.md
archive     → Cleanup                   → moved to archive/
```

## Key mechanisms

**Role reversal — the Socratic method.** The agent doesn't just execute
instructions — it asks questions, challenges decisions, and presents
options with their trade-offs before committing to a direction. It's not
only the developer issuing orders to the agent; the agent pushes back and
drives a dialogue.

**Sub-agents and context management.** Large problems get split into
sub-problems (frontend, backend, storage, infrastructure), each handled by
a sub-agent with its own context window. Sub-agents work independently and
report back with a concise summary, avoiding the problem of one giant
context window getting overloaded with raw exploration output.

**Artifacts with defined interfaces.** Each skill produces and consumes
artifacts in a fixed format. Research produces a document that the
planning skill already expects — no tokens wasted rebuilding context from
scratch at every stage.

**Human in the loop.** The developer keeps their hands on the wheel at
every key moment: choosing between implementation variants, making
architectural calls, reviewing results, and resolving disagreements
between approaches.

**Local artifacts, not global state.** Every change gets its own isolated
folder. There's no single `state.md` that every stage pushes information
into. Benefits: no single point of failure, easy to scale to many
concurrent changes, and if a direction turns out wrong, you delete one
folder with zero impact on the rest of the project.

**Two audiences for the plan.** Planning produces `plan.md` (detailed, for
the agent to execute — roughly 150-300 lines) and `plan-brief.md`
(concise, for the human to review before work starts — under 100 lines).
The agent and the developer need different things from a plan; the
workflow doesn't force one document to serve both.

**Model-switching at review time.** It helps to run the review stage with
a different model than the one that wrote the code — different models
catch each other's blind spots more effectively than a model reviewing
its own work.

## The six command files

Each stage lives in its own file under `.claude/commands/`. Claude Code
picks these up automatically and exposes them as `/new`, `/research`, etc.

### `new.md` → `/new <change-name>`
Kicks off a new unit of work. Reads `CLAUDE.md` for project conventions,
asks 3-5 clarifying questions about the goal, scope, constraints, and
expected test coverage — then waits for your answer before writing
anything. Produces `context/<change-name>/change.md`: goal, in-scope /
out-of-scope, constraints, acceptance criteria, and the raw notes from the
clarifying conversation. This file is the source of truth every later
stage reads from, so it has to be self-contained.

### `research.md` → `/research <change-name>`
Builds understanding of the relevant part of the codebase before any
planning happens. Reads `change.md`, then — for anything touching more
than one area (frontend, backend, storage, CI) — delegates to separate
sub-agents via the `Task` tool, each returning a concise report from its
own context window instead of dumping raw exploration into the main
thread. Produces `research.md`: how the system works today, why it works
that way, key files with line references, risks/pitfalls, and open
questions for planning.

### `plan.md` → `/plan <change-name>`
Turns research into an actionable plan through a Socratic dialogue —
asking more or fewer questions depending on how complex the change turns
out to be, and presenting real trade-offs between implementation options
rather than picking one silently. Produces two files: `plan.md` (detailed,
150-300 lines, written for the agent to execute phase by phase) and
`plan-brief.md` (under 100 lines, written for you to skim before work
starts).

### `implement.md` → `/implement <change-name> [phase]`
Executes the plan phase by phase, running tests/linters after each one
and checking off the "phase verification" items from `plan.md`. Asks
upfront whether to pause for approval after every phase or run straight
through. If reality deviates from the plan mid-implementation, it stops
and asks rather than improvising. Produces working code plus an
`implementation-log.md` that records what happened in each phase and any
deviations from plan.

### `review.md` → `/review <change-name>`
Checks the diff against `plan.md` — not a generic code review, but a
verification that what got built matches what was planned, with a
separate check for code quality and test adequacy. For every issue found,
it asks you directly whether to fix now, accept as debt, or skip — never
fixes silently. Produces `review.md` with a verdict: READY, NEEDS FIXES,
or NEEDS DISCUSSION.

### `archive.md` → `/archive <change-name>`
Closes out the change once review is READY. Appends a final summary to
`change.md`, then moves the whole `context/<change-name>/` folder to
`archive/<change-name>-<date>/`. If recurring problems came up during the
work, it can propose (with your permission) adding a short lesson to
`CLAUDE.md` so future sessions don't repeat the same mistake. Keeps
`context/` limited to active work only, so future sessions don't have to
wade through history that's already settled.

## Why not just prompt harder

A better model gives you a better one-shot, but a good one-shot is still
far from production-ready. The workflow doesn't try to replace judgment
with a bigger model — it structures *when* and *how* human judgment enters
the loop, so it isn't lost between sessions or between team members.

## Tool-agnostic by design

The chain itself — six stages, artifact handoffs, human-in-the-loop
checkpoints — isn't tied to any single coding agent. This implementation
targets Claude Code's native slash commands, but the same six-stage
structure could be re-expressed for a different tool without changing the
underlying workflow. Learn it once, keep it regardless of which agent your
team is using this year.

## Try it: Demo Project

If you want to see this workflow in action without risking a real
project, the repo includes a ready-made `demo-project` — a minimal,
single-file "calculator" (`calc.py`) with all six commands already wired
up in `.claude/commands/`.

The full cycle to test:
```
/new multiply-divide
/research multiply-divide
/plan multiply-divide
/implement multiply-divide
/review multiply-divide
/archive multiply-divide
```

By the end, `calc.py` has two new functions (`multiply()`, `divide()`
with a `ValueError` on division by zero), and
`archive/multiply-divide-<date>/` holds the full decision trail:
`change.md`, `research.md`, `plan.md`, `plan-brief.md`, `review.md`.

It's the fastest way to feel the difference between the workflow and a
plain "add this function for me" — the task is simple enough that all the
attention goes to the mechanics of the chain, not the code itself.

## Adaptation over time

The workflow isn't frozen. Signals from the environment — failing lints,
broken CI, recurring misunderstandings — can be fed back in as short notes
(a "lesson learned" pattern) so future sessions don't repeat the same
mistake. It's meant to be iterated on, not treated as a fixed spec.
