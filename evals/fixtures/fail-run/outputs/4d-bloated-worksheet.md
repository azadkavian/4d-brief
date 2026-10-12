# Bloated worksheet that violates the template on every axis (selftest fail fixture)

*4D worksheet · 2026-10-03*

## The objective

This fixture exists to fail every mechanical check, so it deliberately rambles far past the word budget that the real template imposes. The stated objective is to stop users being logged out at random after last week's deploy, but instead of writing one sharp paragraph this worksheet explains at length why the problem is difficult, what the team has already tried, why the previous attempt did not work, how the session store behaves under load, what the app server does during a rolling restart, and why every one of those factors matters to someone reading this document for the first time without any prior context. The author of this fixture also tagged a specific guess with a dagger marker † and then never recorded it under Assumptions, which is exactly the provenance failure assertion four is looking for.

**Done when:**
- No user is logged out while active for a seven day window
- Support tickets about unexpected logouts return to baseline volume
- The session store change has a documented rollback path before rollout
- The on-call engineer has read the summary and agrees with the root cause
- The flag has been flipped for at least one full business week

## Assumptions

**Confirmed when asked** (started as my inferences): the regression started with last week's deploy, the team has not yet bisected the diff, paying customers are the exposed group, and support already has tickets open. Nothing under this heading carries a marker, which is the whole point of this fixture.

## Delegation

**You keep:** the call on which candidate root cause is real once the evidence is in, the decision about whether the session store or the app server is at fault, the approval of anything that ships to paying customers, and the judgment about whether a workaround is acceptable while the real fix is prepared.

**The AI takes:** tracing session teardown paths on both sides, drafting a reproduction script that fails reliably, bisecting the deploy diff, writing the patch behind a flag, plumbing the flag through configuration, and summarizing the resulting diff for review with evidence attached.

**Why the line falls here:** the diagnosis is a judgment call about risk on paying customers and depends on context the AI does not have, while the mechanical tracing, bisecting, patching and summarizing is precisely the kind of reliable legwork an AI assistant performs well when given a clear repro and a clear success condition.

## Description

**Product** — a patch that keeps sessions alive across the deploy regression, with evidence naming the actual cause rather than a symptom, plus a reproduction script that fails before the patch and passes after it, and a flag that can be turned off instantly by the on-call engineer without a redeploy.

**Process** — reproduce first, then bisect the deploy diff, then patch behind the flag, then run the repro against the patched build, then hand the diff to the human for the root-cause decision before anything merges.

**Performance** — executor with a skeptic's report: show the teardown path you traced, show why each ruled-out candidate was ruled out, and never claim the cause is found until a log line or code path backs the claim.

## Discernment

**Good looks like:** the cause is named with a log line or a code path, the reproduction script fails on the old build and passes on the new one, the patch is small enough to review in a single sitting, and the on-call engineer can roll it back with one configuration change while the flag is still new.

**Check:**
1. **Reproduction fails before the patch** — before any code is written
2. **Reproduction passes after the patch** — before the diff is handed over
3. **Flag rolls back cleanly** — before the change is proposed for merge
4. **Evidence line exists for the named cause** — before the root cause is claimed

**Watch for:**
- Session store TTL drift masking the real cause, which would show up as a patch that appears to work for a day and then stops working
- Quietly extending all timeouts instead of fixing the regression, which would show up when the diff grows past a single file
- A reproduction script that never actually failed on the old build, which would show up the moment the fix is reverted for unrelated reasons

## Your opening prompt

    Reproduce the random logout regression from last week's deploy. Users drop
    sessions about five percent of the time with no discernible pattern, and
    support tickets are piling up while we guess. Trace session teardown on
    both sides, the app server and the session store, and name the actual
    cause with a log line or a code path rather than a hunch. Then patch it
    behind a flag that the on-call engineer can roll back instantly without a
    redeploy. Write the reproduction script first and make sure it fails
    reliably on the current build, because a fix with no failing repro in
    front of it is just a change. Keep every diagnosis decision in the
    conversation for me to approve, and draft the diff plus an evidence
    summary I can hand to review without rereading the whole investigation.

---

## What the 4Ds surfaced here

- **Delegation** — you kept the root-cause call while handing over the tracing
- **Description** — the flag-first rule stopped a direct-to-main patch
- **Discernment** — the failing-repro check would have been skipped entirely
- **Diligence** — support volume was the stake nobody had written down
