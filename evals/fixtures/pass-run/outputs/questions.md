# Question log — flaky-logout-debug (selftest pass fixture)

Persona self-play: Sam, tech lead. Every question asked and the answer chosen.

## Round 1 — Diligence + the objective

**Q1: Diligence — who is affected if this goes out wrong?**
- Paying customers dropped mid-checkout; support tickets are already piling up
- Internal beta users only; nobody outside the company notices
- Our own team, briefly — a rollback fixes it the same day
- Chosen: Paying customers dropped mid-checkout; support tickets are already piling up

**Q2: Diligence — how deep should the fix go before it ships?**
- Deep — name the root cause with evidence, even if it takes a day
- Shallow — extend timeouts now, root-cause it next sprint
- Chosen: Deep — name the root cause with evidence, even if it takes a day

## Round 2 — Delegation

**Q1: Delegation — which part do you keep?**
- I keep the diagnosis call; the AI traces and patches
- The AI diagnoses too; I only review the final diff
- We pair on both until we agree
- Chosen: I keep the diagnosis call; the AI traces and patches

**Q2: Delegation — what outcome would make you wish you had done it yourself?**
- A patch that hides the symptom and the real bug returns Friday
- A slow investigation that ships nothing this week
- Chosen: A patch that hides the symptom and the real bug returns Friday

## Round 3 — Description + Discernment

**Q1: Description — what role should the AI play here?**
- Executor: reproduce, trace, patch, report evidence
- Skeptic: review my hypotheses and poke holes
- Chosen: Executor: reproduce, trace, patch, report evidence

**Q2: Discernment — how will you know the result is good?**
- A named cause with a log line, repro green before the patch
- Feels right after a week without tickets
- Chosen: A named cause with a log line, repro green before the patch

**Q3: That's enough — write it up with your best guesses for the rest?**
- Not yet — one more round on assumptions
- Yes, best guesses are fine for the rest
- Chosen: Not yet — one more round on assumptions

## Round 4 — Assumptions (one question per assumption, each option a position)

**Q1: Assumptions — what idle timeout are sessions set to?**
- 30 minutes, then drop the session
- 60 minutes, then drop the session
- Chosen: 30 minutes, then drop the session

**Q2: Assumptions — how does the fix ship?**
- Behind a `logout_fix` flag with instant rollback
- Straight to main; we roll back by redeploying
- Chosen: Behind a `logout_fix` flag with instant rollback

**Q3: Assumptions — what counts as fixed?**
- A full week with zero involuntary logouts
- Two clean days, then flip the flag
- Chosen: A full week with zero involuntary logouts
