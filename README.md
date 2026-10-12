# 4d-brief

`4d-brief` is a skill that turns a raw, half-formed idea into a clear brief before you hand work to an AI assistant. It runs a short guided dialogue — a silent strawman, three or four question rounds, a mandatory assumption check — and leaves you with a worksheet you act from; the worksheet is the deliverable, not the task itself. It is for anyone who arrives with a fuzzy idea ("the pricing page feels off", "I don't trust AI with this board update") and wants help scoping what to delegate, what role the AI should play, and how they'll check the result.

## How a run goes

Excerpt from [`skills/4d-brief/examples/walkthrough.md`](skills/4d-brief/examples/walkthrough.md):

```markdown
**User types:** `/4d-brief I want to add rate limiting to our API`

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
```

Rounds 2–3 cover Delegation and then Description + Discernment, round 4 is the mandatory assumption check, and the run ends with a worksheet file and a short hand-off.

## Install

**Claude Code** — link (or copy) the skill folder into your skills directory:

```bash
ln -s <repo>/skills/4d-brief ~/.claude/skills/4d-brief
```

**OpenCode** — same `~/.claude/skills/` discovery: link (or copy) the folder the same way. No skill edits are needed — the skill asks its questions through the harness's question tool and uses OpenCode's `question` tool automatically in place of Claude Code's `AskUserQuestion`.

## What gets measured

The behavioral benchmark compares runs **with the skill** against a **baseline** (a frozen pre-change snapshot of the same skill): 18 runs, pass rate = the 9 benchmark assertions per run. Summary row copied verbatim from [`docs/benchmark.md`](docs/benchmark.md):

| Metric | With Skill | Without Skill | Delta |
|--------|------------|---------------|-------|
| Pass Rate | 98% ± 5% | 99% ± 4% | -0.01 |

See [`docs/benchmark.md`](docs/benchmark.md) for methodology, time and token results, and notes on the recorded failures. Beyond pass rate, runs **with the skill** finished ~22% faster and used ~22% fewer tokens, and description optimization lifted natural-language trigger accuracy from 85% to 95% on a 20-query eval set — both documented in the same file.

## Attribution

The 4D framework (Delegation, Description, Discernment, Diligence) derives from **Anthropic's AI Fluency** work. This skill rephrases and applies those concepts; see Anthropic's materials for the original framework.

Sources: [AI Fluency: Framework & foundations (Anthropic Academy)](https://academy.claude.com/courses/ai-fluency-framework-foundations) · [The AI Fluency Framework (Dakan & Feller)](https://aifluencyframework.org/)

## License

MIT — see [`LICENSE`](LICENSE).
