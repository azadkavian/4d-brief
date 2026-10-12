# Skill Benchmark: 4d-brief

**Model**: a frontier-class model via a local provider (single model across all runs)
**Date**: 2026-10-03T14:46:49Z
**Evals**: 1, 2, 3 (3 runs each per configuration)

## Summary

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 98% ± 5% | 99% ± 4% | -0.01 |
| Time | 478.6s ± 97.3s | 613.7s ± 113.8s | -135.1s |
| Tokens | 72972 ± 13595 | 93662 ± 14279 | -20690 |

## Notes

- 18 runs total: 3 evals × {with_skill, without_skill} × 3 runs, executed as fresh
  agent sessions in persona self-play (the "user" answers the skill's questions as a
  scripted persona). `with_skill` reads the skill from this repo; `without_skill`
  runs from a frozen pre-change snapshot of the same skill.
- Pass rate = the 9 benchmark assertions per run (162 judgments total): worksheet
  placement/length/sections/assumption-daggers, question-round limits, option
  quality, progress markers, and handoff brevity. Assertions 1–6 graded by
  `evals/check_assertions.py` (deterministic), 7–9 by an independent grader agent
  that was not told which config produced which run.
- Time is self-measured per run; tokens are the session's input+output+reasoning
  totals read from the harness session store (the harness does not expose them to
  the run itself).
- The three failures are recorded unmodified in the raw results: one assertion-6
  hit is a pattern match inside the run's own compliance sentence (kept as a
  failure — the check is a mechanical text match by design), one dangling
  dagger-marker worksheet, one over-long baseline handoff.
- Interpretation: behavioral output quality is at parity (the modernization did
  not change the framework content), while the skill makes runs ~22% faster and
  ~22% cheaper. Trigger-rate gains are measured separately (see
  `4d-brief` trigger evaluation, 85% → 95% on a 20-query held-in/held-out set).
