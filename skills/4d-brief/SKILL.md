---
name: 4d-brief
description: >-
  Use this skill when the user wants help turning a fuzzy idea into a clear brief before
  handing work to an AI assistant. Signals: invoking /4d-brief, asking to think something
  through in 4D, or arriving with a half-formed idea ("the pricing page feels off", "I
  don't trust AI with this board update") and needing help scoping what to delegate, what
  the AI's role should be, and how they'll check the result. Run a short guided dialogue
  and leave them with a worksheet they act from — the worksheet is the deliverable, not
  the task itself. Do NOT use for questions about this skill's mechanics or past runs
  (where files are saved, what a previous worksheet said), for the actual work being
  delegated (code, prose, review, debugging), or for general opinions about AI in the
  abstract.
---

# 4D

The user arrives with a raw, half-formed idea. Help **them** think it through in the 4D
framework, then leave them with a worksheet they can act from.

**You are not doing the task.** You are not planning the implementation either — that comes
after, and usually in a fresh conversation. You are clarifying *what the objective actually is*
and *how the human and an AI assistant should divide and check the work*.

**You are not thinking for them.** You draft; they decide. Every question you ask carries your
best guess so they can correct rather than compose. But the decisions are theirs — especially
stakes, quality bar, and what they will own afterwards.

Works for any kind of task — code, writing, research, a decision, a conversation to prepare for.
Nothing here is coding-specific, and you must not make it so.

It must also work for someone who has never heard of the 4Ds. They learn the framework by being
walked through it, one named D at a time, without a lecture.

---

## The flow

### Phase 0 — Intake

Read the raw idea. Ask yourself only: *can I draft a plausible first pass at all four Ds from
this?*

- **Yes** → go straight to Phase 1. Most ideas land here, even vague ones.
- **No** — it is a bare noun phrase with no discernible outcome ("the auth thing", "marketing")
  → spend one round asking what they are trying to achieve and what prompted it, then continue.

Do not research. Do not read the codebase, search the web, or explore files. This is about the
user's intent, not the domain. If the idea references something you would need to look up, that
is a fact for the worksheet to flag, not for you to resolve now.

Read `reference/framework.md` before the first round if you need the sub-components fresh.

### Phase 1 — Strawman (silent)

Draft a first-pass answer to all four Ds from the raw idea alone. Guess. Commit to specifics.

This is the engine of the whole skill. Because you have a strawman, every question becomes
*"here is my read, correct me"* rather than a blank prompt — which is the difference between a
dialogue that takes two minutes and one the user abandons.

> **A guess generates a question. A guess does not fill the worksheet.**
>
> This is the single most important rule in this skill. Anything you invented — a standard, a
> threshold, a tool, a convention, a quality bar — is a candidate for Round 4 or for the
> `Assumptions` section. It never appears in the finished worksheet as though the user chose it.
>
> A user answering *"how much does that matter?"* has confirmed a **weight**, not authored a
> **claim**. Keep that distinction; it is easy to lose.

Never show the raw strawman. It becomes the options.

### Phase 2 — Question rounds

**3–4 rounds. Hard cap 5.** Each round is one call to the harness's structured question tool (AskUserQuestion in Claude Code, question in OpenCode), carrying 2–3 questions.

| Round | Covers | Why here |
|---|---|---|
| 1 | **Diligence** + the objective | Stakes first: they set how deep everything after should go. Who is this really for, and who is affected if it is wrong. |
| 2 | **Delegation** | What they keep vs. hand over, and what outcome would make them wish they had done it themselves. You supply platform awareness — what an AI assistant is genuinely good and bad at *for this task*. They own problem awareness. |
| 3 | **Description** + **Discernment** | What role the AI should play, how much process to prescribe, and what they will check to know it worked. |
| 4 | **Assumptions** | Mandatory. See below. |

Rounds 1–3 adapt: skip or merge any whose answers are already settled by the idea or by earlier
answers. Round 4 does not adapt away unless the strawman genuinely invented nothing material,
which is rare.

From **round 3 onward**, include a way out — an option along the lines of *"that's enough, write
it up with your best guesses for the rest."* Honour it immediately. Round 4 still runs; it is
short, and it is the safety net that makes "your best guesses" safe to say yes to.

### Round 4 — the assumption check

Before writing anything, put the specifics you are about to commit **in their name** through a
real decision.

**Never offer an option that means "these are all fine."** A round with a rubber-stamp option
gets rubber-stamped — that is not a risk, it is what happened the first time this round shipped.
A batch approval is not authorship, and a worksheet built on one click is exactly the failure
this round exists to prevent.

So: **one question per assumption, and every option is a different version of the commitment.**
Confirmation becomes selection. Whatever they pick is genuinely theirs, because there was no way
to pick nothing.

One question-tool call carrying 2–3 single-select questions:

> **Contrast — what bar are you actually holding this to?**
> - WCAG AA, the standard
> - AA, plus AAA where it happens to be easy
> - AAA throughout, even where it constrains the design
>
> **Design directions — how many do you want to choose between?**
> - Two or three, properly different from each other
> - One considered proposal, iterated
> - As many as it takes until something lands

Rules:

- **No option may mean "I didn't read this."** Every option is a position someone could defend.
- The most likely option goes first — so picking it is still a decision, not a default.
- 2–3 questions, the most load-bearing guesses only. Pick the ones that change the work if wrong.
- State each option as **the commitment it would become**, not as a topic. *"AAA throughout"*,
  not *"contrast approach"*.

Everything the strawman invented that there was no room to ask about goes into the worksheet
marked `†` and listed under `Assumptions`.

Everything asked here keeps its provenance too: it became their decision, but it started as your
inference, and `Assumptions` records that in one line. See `reference/template.md`.

### Phase 3 — Write the worksheet

Save the worksheet as `4d-<slug>.md` in the directory where the session was launched (the workspace root shown in the environment info), where `<slug>` is 2–4 kebab-case words from the refined objective. Build an absolute path from that directory. Never write it into this skill's own folder or the home folder, unless the session was actually launched there. Follow `reference/template.md` — including its word budgets, which exist because the first version of this skill produced a worksheet nobody would re-read.

### Phase 4 — Hand off

Close with a short message: where the file is, the single sharpest thing the dialogue clarified,
and an offer to start the first delegated piece using that framing. Do not restate the document.

---

## Writing the questions

This is the hardest part of the skill and where the quality lives. A generic question round makes
the whole thing feel like a form; a specific one feels like a colleague who was paying attention.

**Options are generated fresh for this idea. Never templated.**

| Bad — a label | Good — a consequence |
|---|---|
| High stakes | Goes to customers Friday; a mistake is public |
| Low stakes | Internal spike — if it is wrong we throw it away |
| Needs accuracy | Finance will act on these numbers without re-checking |
| Some autonomy | Make the call yourself; tell me what you chose and why |

The user should recognise their situation at a glance, without translating jargon.

**Name the D in the question, in one clause.** This is how a first-timer learns the framework.

- *"Delegation — which part of this do you want to keep doing yourself?"*
- *"Description — what role should the AI play here?"*
- *"Discernment — how will you know the result is actually good?"*
- *"Diligence — who is affected if this goes out wrong?"*

**Ask only what cannot be inferred.** These are genuinely unknowable from a raw idea, and are
where your question budget should go:

- the real stakes and who is exposed
- what "good enough" means to *them*
- the role they want the AI to play
- what they would hate — the outcome that would make them wish they had done it themselves
- what they already tried

Nearly everything else you can guess — and then must put through Round 4.

**Mechanics.** 2–4 options per question, most likely first. The tool's own free-text escape ("Other" / "Type your own answer") is automatic — never add your own.
Never ask a question whose answer changes nothing in the worksheet.

---

## Progress marker

Your instructions load once, but the dialogue spans several turns. Emit this line at the end of
every dialogue turn, and re-read it before each round so the flow survives an interruption or a
tangent:

```
4D · ✓ Diligence  ✓ Delegation  → Description  · Discernment  · Assumptions
```

`✓` settled · `→` in progress · `·` not yet reached.

If the user derails into the task itself mid-dialogue, follow them briefly, then return with the
marker and the next question.

---

## Reference

- `reference/framework.md` — the four Ds and their sub-components
- `reference/template.md` — the worksheet structure, voice rule and word budgets
- `examples/walkthrough.md` — one end-to-end run, raw idea to finished worksheet
