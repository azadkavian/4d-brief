---
title: 4d worksheet - stop random logouts
date: 2026-10-03
---

# Stop random user logouts after the last deploy

*4D worksheet · 2026-10-03*

## The objective

Cut random session drops to zero for paying users. Since last week's deploy about 5% of sessions die at random with no pattern; the fix must stop the drops without regressing the login flow †. Done when: no user is logged out while active, logout tickets stop for a week, and the session change ships behind a flag.

**Done when:**
- No involuntary logouts in a 7-day window with the flag on
- Support ticket volume on logouts back to baseline
- Rollback path documented before the flag flips

## Assumptions

**Confirmed when asked** (started as my inferences): the regression started with last week's deploy · you keep every diagnosis decision · paying customers are the exposed group

**Still mine, not yours** — every `†` in the body has a line here:
- † 30-minute idle timeout on sessions — change to 60 if checkout flows run longer
- † Ship behind a flag with instant rollback — if there is no flag plumbing, ship dark first and flip next week

## Delegation

**You keep:** choosing the root cause once the evidence is in, deciding whether the session store or the app server is at fault, approving what ships.

**The AI takes:** tracing session teardown paths, drafting the reproduction script, writing the patch and the flag plumbing, summarizing the diff for review.

**Why the line falls here:** the diagnosis is a judgment call about risk on paying customers; the mechanical tracing and patch work is what an AI assistant does reliably.

## Description

**Product** — a patch that keeps sessions alive across the deploy regression, with evidence naming the actual cause, not a symptom.

**Process** — reproduce first, then bisect the deploy diff, then patch behind the `logout_fix` flag; no flag, no merge.

**Performance** — executor with a skeptic's report: show the teardown path you traced and why each candidate was ruled out.

## Discernment

**Good looks like:** the cause is named with a log line or code path, and the fix is small enough to review in one sitting †.

**Check:**
1. **Repro before patch** — *before any code changes*
2. **Flag can roll back** — *before merge*

**Watch for:**
- Session store TTL drift masking the real cause — *when the patch touches TTLs*
- Quietly extending all timeouts — *when the diff grows past one file*

## Diligence

**Stakes:** paying customers are dropped mid-session; visible through support tickets.

**Disclosure:** support and the on-call engineer are told AI drafted the patch.

**You own:** the root-cause call and the merge decision.

## Your opening prompt

    Reproduce the random logout regression from last week's deploy: users drop
    sessions ~5% of the time with no pattern. Trace session teardown on both
    sides (app server and session store), name the cause with a log line or
    code path, and patch it behind a `logout_fix` flag that can be rolled back
    instantly. Repro script first, no patch without it. Keep diagnosis
    decisions in the conversation; draft the diff and the evidence summary.

---

## What the 4Ds surfaced here

- **Delegation** — you kept diagnosis, not implementation
- **Description** — the skeptic's report rule forced evidence before patch
- **Discernment** — the repro-before-patch check would have been skipped
- **Diligence** — support volume was the stake nobody had named
