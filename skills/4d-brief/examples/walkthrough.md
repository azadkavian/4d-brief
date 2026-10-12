# Walkthrough: one end-to-end run

Shows the texture the questions should have. The point is not this task — it is that every
option names a *consequence the user recognises*, and nothing generic appears anywhere.

**User types:** `/4d-brief I want to add rate limiting to our API`

---

## Phase 1 — strawman (never shown)

> Probably a public API with an abuse or cost problem. Likely wants per-key limits. The
> interesting unknowns: is this reacting to an incident (urgent, narrow) or hardening (broad)?
> Who gets locked out if the limit is wrong? Do they already have a gateway that does this?
> Delegation line probably: they choose the limits and the policy, AI writes the middleware.
>
> Specifics I am inventing and must not write into their objective unchallenged: token bucket
> over fixed window, per-API-key rather than per-IP, `429` with `Retry-After`, limits applied at
> the edge rather than in the app, a staged rollout behind a flag.

Three real unknowns about intent, five invented specifics. The unknowns become rounds 1–3; the
inventions become round 4.

## Round 1 — Diligence + objective

> **Diligence — what happens if the limit is set wrong and real users get blocked?**
> - Paying customers hit it and file tickets within the hour
> - Only internal services affected; we would notice and fix quietly
> - Nothing is live yet — this ships behind a flag
>
> **What is prompting this now?**
> - One client is hammering us and costs are climbing
> - Hardening before a launch; no incident yet
> - A security or compliance review asked for it

They pick *paying customers within the hour* and *one client hammering us*.

That changes everything downstream: urgent, narrow, high blast radius. The delegation line pulls
back toward the human on the policy, and Discernment needs a real verification step.

## Round 2 — Delegation

> **Delegation — where do you want the line?** *(you know your traffic; I do not)*
> - You set the limits and the policy; I write the implementation
> - I propose limits from your logs, you approve before anything ships
> - You want the whole thing including the numbers — you will sanity-check at the end
>
> **What outcome would make you wish you had done this yourself?**
> - A legitimate customer gets throttled and we do not find out for days
> - It works but nobody can explain the numbers when asked
> - It quietly does not apply to the traffic that actually caused the problem

They pick *I propose, you approve* and *legitimate customer throttled silently*.

The second answer is doing real work: it makes observability a requirement, not a nice-to-have,
and it writes itself straight into Discernment.

## Round 3 — Description + Discernment

> **Description — what role should I play while we do this?**
> - Skeptic: push back on the approach before writing anything — this touches live traffic
> - Executor: I write it, you review the diff
> - Pair: think it through together as we go
>
> **Discernment — what will you actually check before this goes live?**
> - Replay real traffic against the limiter and see who would have been blocked
> - Read the code and reason about it; we do not have replay tooling
> - Ship behind a flag to one client and watch
>
> **Want to keep going, or is that enough?**
> - Keep going — one more round
> - That is enough, write it up with your best guesses

They pick *skeptic*, *replay real traffic*, and *keep going*.

## Round 4 — the assumption check

Mandatory, and it runs even if they had chosen "that is enough". This is where the invented
specifics get their moment — as **decisions, not approvals**. Two of the five guesses are
load-bearing enough to ask about:

> **What are the limits actually keyed on?**
> - The API key — authenticated callers, one budget each
> - The client IP — catches unauthenticated traffic too, but shared NATs share a budget
> - Both, with different ceilings
>
> **Where does the limiter run?**
> - In the app, alongside the routes it protects
> - At the gateway, before traffic reaches the app
> - At the CDN edge, before it reaches your infrastructure

They pick *client IP* and *in the app* — it turns out the abusive traffic is unauthenticated, and
they have no gateway to put anything in front of.

Both guesses were wrong, and neither question let them say "fine, whatever". Had this round
offered *"These are all fine"*, both errors would have sailed into the worksheet as the user's own
decisions and surfaced at implementation time instead.

The three specifics not asked about — token bucket, `429` with `Retry-After`, staged rollout — go
into the worksheet marked `†` and listed under `Assumptions`. The two decided here are recorded
too, on the "confirmed when asked" line: they are the user's now, but they started as guesses.

---

## What made this work

**The strawman did the heavy lifting.** Six plausible facts were guessed, so the questions could
spend their budget on what was genuinely unknowable.

**Every option is recognisable.** "Paying customers file tickets within the hour" is something
you either recognise or you do not. "High stakes" is something you have to interpret.

**The Ds are named but not explained.** The user learns that *Diligence* means "who gets hurt" by
watching it be used that way — no definition given, none needed.

**Round 4 caught two errors.** That is the round's entire justification, and it will usually
catch at least one.

---

## Counter-examples

**A bad content round:**

> **Delegation — how much should the AI do?**
> - A lot
> - Some
> - A little

No consequence, no specificity, nothing learned, and the answer changes nothing in the
worksheet. If a round could be asked about any task at all, it is the wrong round.

**A bad assumption round** — this is the real one, observed on a live run, not a hypothetical:

> **Assumptions — which of these should I change?** *(multi-select)*
> - These are all fine
> - AAA contrast wherever feasible
> - 2–3 design directions to choose between
> - Works down to 320px

The user clicked **"These are all fine."** Every guess passed, the worksheet then declared
*"Nothing material — everything below is yours,"* and four inferences became the user's stated
objective on the strength of one click.

The wording was not the problem; the shape was. **An option meaning "I didn't read this" will be
chosen, because it is the cheapest one on the screen.** Ask one question per assumption, make
every option a position someone could defend, and there is nothing cheap to click.

The same failure in smaller form — topics instead of commitments:

> - Performance targets
> - Error handling approach

The user cannot tell what they would be agreeing to. State the claim: *"Over-limit returns `429`
with `Retry-After`"*.
