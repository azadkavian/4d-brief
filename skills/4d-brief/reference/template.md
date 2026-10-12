# Worksheet template

Written to `4d-<slug>.md` in the folder where the session was launched (see SKILL.md, Phase 3). The reader is the **human**, about to hand work to an AI assistant.

## Four rules that override everything else

**1 · Operational, not essayistic.** A filled-in worksheet, not a reflection on the framework.
Every line should be something they can act from. If a section has nothing real in it for this
task, say so in one line — do not pad.

**2 · Voice.** The worksheet body is **second person** throughout ("You keep", "You'll check",
"You own"). The opening prompt block is **first person** — that is the user speaking to the
assistant. Never mix within a section.

**3 · One home per fact.** Within the body, every fact appears in exactly one section. The order
of work lives in *Process* and nowhere else; the quality bar lives in *Product* and nowhere else.
The opening prompt is a **rendering** of the body and may restate anything — that is its job. It
is kept honest by its word budget, not by this rule.

**4 · Mark what you guessed.** Any specific the user did not author gets recorded under
`Assumptions` — including ones they chose in Round 4, which became their decision but started as
your inference. A user who answered *"how much does that matter?"* confirmed a weight, not a
claim.

## Length

**The whole file must come in under 850 words. This is the rule.** The per-section budgets below
are guides that help you get there — budgets that do not sum to a ceiling can all be satisfied
while the file grows, which is exactly what went wrong before.

| Section | Guide |
|---|---|
| The objective | ≤ 120 words, including any `Done when:` bullets |
| Assumptions | ≤ 40 words |
| Delegation | ≤ 100 words |
| Description | ≤ 100 words across all three levels |
| Discernment | ≤ 140 words |
| Diligence | ≤ 70 words |
| Before you start | ≤ 40 words |
| Your opening prompt | ≤ 180 words *(provisional — see below)* |
| What the 4Ds surfaced | ≤ 60 words |
| Collapsed glossary | ≤ 50 words |

**When you are over 850, cut in this order:** the opening prompt, then "Watch for", then the
glossary. **Never** the objective or Assumptions — those are the two sections the whole document
exists for.

> The 180-word prompt budget is provisional. It was set by reading finished worksheets, not by
> anyone pasting one into a real session. If a prompt block genuinely needs more to be usable,
> that is evidence to revise this number, not a licence to ignore it.

Write in their words where you can; it is what they will recognise later.

---

```markdown
# <Refined objective as a title>

*4D worksheet · <date>*

## The objective

One paragraph. What is actually being achieved and any constraint that shapes everything else.
Often the most valuable part of the document — the raw idea rarely said what done means. It must
be sharper than what they typed.

**Done when:**
- <criterion>
- <criterion>
- <criterion>

<Use the bullets whenever done-ness has more than one condition. Never announce a list in the
prose and then write it as prose.>

## Assumptions

Where the specifics came from. Two kinds, both recorded:

**Confirmed when asked** (started as my inferences): <thing> · <thing> · <thing>

**Still mine, not yours** — every `†` in the body has a line here:
- † <The commitment, stated plainly.> — <what to change it to if wrong>

<If the strawman genuinely invented nothing — rare — write "Nothing material; all of this is
yours." Do not write that merely because Round 4 went smoothly.>

## Delegation

**You keep:** <the judgment calls, the decisions only they can make, the parts where their
context is the scarce input>

**The AI takes:** <the concrete work being handed over>

**Why the line falls here:** <one or two sentences — usually about stakes, or about what the AI
is unreliable at for this particular task>

<No order-of-work line here. Sequence belongs to Process.>

## Description

**Product** — <what done looks like, and the one or two constraints that decide it. The full
requirement list lives in the prompt block; name the shape here, do not restate it.>

**Process** — <the route: sequence, checkpoints, what must happen before what. This is the only
place the order of work is written. Or "no constraint — any sound route is fine".>

**Performance** — <the role: skeptic / pair / executor / editor / tutor. Plus any behavioural
rule that traces from the stakes above — this is usually the highest-value line in the
worksheet.>

## Discernment

**Good looks like:** <the criteria, decided now rather than after>

**Check:**
1. **<Check>** — *<when>*
2. **<Check>** — *<when>*

**One moment per line.** A check with a compound trigger ("after each step, and once before
ship") is two checks — split it, or it will be half-done. A check you cannot tick is not a check.

**Watch for:**
- <failure mode specific to this task> — *<when it would show up>*
- <…>

Same rule as the checks: a failure mode with no moment attached gets read once and forgotten.

## Diligence

**Stakes:** <who is affected if this is wrong, and how visibly>

**Disclosure:** <who needs to know AI was involved — or "nothing needed here">

**You own:** <what must be verified before this goes anywhere>

## Before you start

Decisions the prompt below leaves blank — these are yours, and they are the same things
Delegation said you keep:

- **[PLACEHOLDER]** — <what you need to decide, in one line>

<Omit this whole section if the prompt block has no placeholders. Do not pad it.>

## Your opening prompt

    <A ready-to-paste block carrying the objective, the requirements, the behavioural rules and
    the first step. First person, in their voice. It may restate anything from the body — but it
    is the first thing cut when the file runs long, so every line must earn its place.>

---

## What the 4Ds surfaced here

One line per D, naming what it caught *on this task* that they would not otherwise have written
down. If a line would be true of any task, it is the wrong line.

- **Delegation** — <what the split revealed>
- **Description** — <the rule that would not have been stated>
- **Discernment** — <the check that would have been skipped>
- **Diligence** — <the stake that was not being looked at>

<details>
<summary>What the 4Ds are</summary>

**Delegation** — what to hand over and what to keep, given the goal and the tool.
**Description** — what you want out, how to get there, and how the AI should behave.
**Discernment** — is the output good, was the approach sound, is it collaborating well.
**Diligence** — whether to build it, who to tell, and verifying before it ships.

From Anthropic's AI Fluency framework.
</details>
```
