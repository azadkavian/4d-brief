#!/usr/bin/env python3
"""Mechanical grading for the 4d-brief behavioral benchmark (assertions 1-6).

Usage
-----
    python3 evals/check_assertions.py <run_dir>

<run_dir> is one run's directory, i.e. one benchmark run directory (the
project's gitignored dev workspace, not shipped), layout
eval-<eval_name>/<config>/run-<N>/. Per the run
prompt, the worksheet is written at the run dir root (the run's designated
workspace root) and every other output lives under <run_dir>/outputs/,
including <run_dir>/outputs/questions.md.

Output contract
---------------
Prints exactly one JSON object to stdout:

    {"expectations": [{"text": <assertion string>, "passed": <bool>,
                       "evidence": <file:line or quote>}, ...]}

covering assertions 1-6 in order. The `text` strings are read from
evals/evals.json (sibling of this script) at runtime - they are never retyped
here, so they stay byte-identical to the benchmark's assertion texts.
Assertions 7-9 are judged later by a separate grader subagent, not by this
script. Exit status: 0 whenever the JSON was produced (checks may fail - that
is data, not an error); 2 for usage/parse errors (message on stderr).

File references in `evidence` are relative to <run_dir>. For "not found"
checks the evidence instead names the path/pattern searched.

Grading split: assertions 1-4 are mechanical checks against the run dir and the
worksheet; assertions 5-6 are mechanical checks against outputs/questions.md.

Interpretations (binding for this checker)
------------------------------------------
* Assertion 1 - the worksheet must be exactly one `4d-*.md` file directly in
  the run dir root. If none is at the root but one exists deeper in the run
  dir, assertion 1 fails (wrong place) and assertions 2-4 are still evaluated
  against that file so each assertion reports on its own merits. If no
  `4d-*.md` exists anywhere under the run dir, assertions 1-4 all fail with
  search evidence. The "not in the skill folder or home directory" clause is
  enforced by construction: the run's designated workspace root IS <run_dir>.
* Assertion 2 - "body is under 850 words" means: strip a leading YAML
  frontmatter block (only when the file's first line is exactly `---`, remove
  through the next line that is exactly `---`), then count words on the
  remainder as `wc -w` does - whitespace-separated tokens, so punctuation
  glued to a word does not split it and standalone markdown tokens (`---`,
  `|`) each count as one token. Pass iff count < 850 (strictly under 850).
* Assertion 3 - the seven section names from the assertion text are matched
  case-insensitively against `^## <name>$` headings (trailing `#`s and
  whitespace ignored).
* Assertion 4 - a `dagger` marker "resolves to a line under Assumptions" when
  the `## Assumptions` section (up to the next `##` heading) contains at least
  as many `dagger`-bearing lines as the rest of the body. Body markers beyond
  that count are cited as unresolved. Zero body markers passes vacuously.
* Assertion 5 - rounds are detected with the case-insensitive regex
  `round\\s*[#:-]?\\s*(\\d+)` anywhere in outputs/questions.md; the round count
  is the highest round number found (0 markers fails: <=5 rounds cannot be
  confirmed from an unlabelled file). "Round 4 ran with single-select
  questions" is checked conservatively: the text from the Round 4 marker to
  the next higher round marker (or EOF) must contain no explicit multi-select
  phrasing (`multi-select`, `select/choose all`, `all of the above`,
  `select/choose multiple`, `more than one option`, `any number of`); a
  missing Round 4 marker fails. A recording that simply never writes
  multi-select phrasing passes - this is a lint, the grader judges nuance.
* Assertion 5-6 input - only <run_dir>/outputs/questions.md is read. If it is
  missing, both fail with evidence naming the path searched.
* Assertion 6 - the whole of outputs/questions.md is searched
  case-insensitively for `all fine` or `didn't read this` (also `did not read
  this`, straight/curly apostrophes). Any match - offered option, question or
  answer line - fails, because no offered option anywhere may mean that.

Self-test fixtures (kept)
-------------------------
Hand-made fixtures ship with this repository and are kept for
regression re-runs:

    evals/fixtures/pass-run/   -> expected 6/6 pass
    evals/fixtures/fail-run/   -> expected 6/6 fail,
        each of the six assertions failing for its own distinct reason
       (worksheet misplaced, >850 words, missing section, dangling `dagger`,
        6 rounds + a multi-select Round 4, an "all fine" option)

Reproduce: python3 evals/check_assertions.py <that-dir>
"""

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
EVALS_PATH = SCRIPT_DIR / "evals.json"

SECTION_NAMES = [
    "The objective",
    "Assumptions",
    "Delegation",
    "Description",
    "Discernment",
    "Diligence",
    "Your opening prompt",
]

HEADING_RX = re.compile(r"^##\s+(.+?)\s*$")
ROUND_RX = re.compile(r"\bround\s*[#:\-]?\s*(\d+)", re.IGNORECASE)
MULTI_RX = re.compile(
    r"multi[-\s]?select|multiselect|select\s+all(?:\s+that\s+apply)?"
    r"|choose\s+all(?:\s+that\s+apply)?|select\s+multiple|choose\s+multiple"
    r"|all\s+of\s+the\s+above|more\s+than\s+one\s+option|any\s+number\s+of",
    re.IGNORECASE,
)
BAD_OPTION_RX = re.compile(
    r"all\s+fine|didn['\u2019]?t\s+read\s+this|did\s+not\s+read\s+this",
    re.IGNORECASE,
)

DAGGER = "\u2020"  # †


def die(message):
    sys.stderr.write("error: %s\n" % message)
    raise SystemExit(2)


def load_assertions():
    """Read the 9 assertion strings from evals.json (never retyped here)."""
    try:
        raw = EVALS_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        die("cannot read %s: %s" % (EVALS_PATH, exc))
    try:
        data = json.loads(raw)
    except ValueError as exc:
        die("%s is not valid JSON: %s" % (EVALS_PATH, exc))
    assertions = data.get("assertions")
    if not isinstance(assertions, list) or len(assertions) != 9:
        die("%s: expected a list of 9 assertion strings, got %r"
            % (EVALS_PATH, type(assertions).__name__))
    return assertions


def rel(path, run_dir):
    try:
        return str(path.relative_to(run_dir))
    except ValueError:
        return str(path)


def find_worksheets(run_dir):
    """Return (root_matches, all_matches) for 4d-*.md, files only."""
    root = sorted(p for p in run_dir.glob("4d-*.md") if p.is_file())
    deep = sorted(p for p in run_dir.rglob("4d-*.md") if p.is_file())
    return root, deep


def pick_worksheet(root, deep):
    """Worksheet used by checks 2-4: root match if any, else deepest find."""
    if root:
        return root[0]
    for path in deep:
        if path not in root:
            return path
    return None


def strip_frontmatter(text):
    """Drop a leading YAML frontmatter block; return (body, offset_lines)."""
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return "\n".join(lines[i + 1:]), i + 1
    return text, 0


def read_worksheet(ws):
    return ws.read_text(encoding="utf-8", errors="replace")


NO_WORKSHEET = (
    "no 4d-*.md found to inspect (searched 4d-*.md at the run dir root, "
    "then recursively under the run dir)"
)


# ---------------------------------------------------------------------------
# Assertion 1 - worksheet at the run dir root as 4d-<slug>.md
# ---------------------------------------------------------------------------

def check_1(run_dir, root, deep):
    if len(root) == 1:
        return True, "%s:1 worksheet present at the run dir root" % rel(root[0], run_dir)
    if len(root) > 1:
        names = ", ".join("%s:1" % rel(p, run_dir) for p in root)
        return False, ("multiple worksheets at the run dir root (%s); "
                       "expected exactly one 4d-<slug>.md" % names)
    others = [p for p in deep if p not in root]
    if others:
        names = ", ".join("%s:1" % rel(p, run_dir) for p in others)
        return False, ("no 4d-*.md at the run dir root; found elsewhere instead: "
                       "%s (searched 4d-*.md at the run dir root, then recursively)"
                       % names)
    return False, ("no 4d-*.md found at the run dir root or anywhere under it "
                   "(searched 4d-*.md at the run dir root, then recursively)")


# ---------------------------------------------------------------------------
# Assertion 2 - body under 850 words (excluding YAML frontmatter, wc -w tokens)
# ---------------------------------------------------------------------------

def check_2(run_dir, ws):
    if ws is None:
        return False, "no worksheet found to measure - " + NO_WORKSHEET
    body, offset = strip_frontmatter(read_worksheet(ws))
    words = len(body.split())
    passed = words < 850
    evidence = ("%s:%d body word count %d (YAML frontmatter excluded; wc -w-style "
                "tokens) - %s 850"
                % (rel(ws, run_dir), offset + 1, words,
                   "under" if passed else "NOT under"))
    return passed, evidence


# ---------------------------------------------------------------------------
# Assertion 3 - all seven ## sections present
# ---------------------------------------------------------------------------

def check_3(run_dir, ws):
    if ws is None:
        return False, "no worksheet to inspect - " + NO_WORKSHEET
    lines = read_worksheet(ws).splitlines()
    found = {}
    for i, line in enumerate(lines, start=1):
        m = HEADING_RX.match(line)
        if not m:
            continue
        name = m.group(1).strip().rstrip("#").strip().lower()
        if name in {s.lower() for s in SECTION_NAMES} and name not in found:
            found[name] = i
    missing = [s for s in SECTION_NAMES if s.lower() not in found]
    found_lines = [found[s.lower()] for s in SECTION_NAMES if s.lower() in found]
    where = rel(ws, run_dir)
    if not missing:
        return True, ("%s:%s all seven '## ' sections present"
                      % (where, ",".join(str(n) for n in found_lines)))
    return False, ("%s:%s - missing '## ' section(s): %s (searched '^## ' headings)"
                   % (where, ",".join(str(n) for n in found_lines) or "none",
                      ", ".join(missing)))


# ---------------------------------------------------------------------------
# Assertion 4 - every † marker in the body resolves to a line under Assumptions
# ---------------------------------------------------------------------------

def check_4(run_dir, ws):
    if ws is None:
        return False, "no worksheet to inspect - " + NO_WORKSHEET
    body, offset = strip_frontmatter(read_worksheet(ws))
    body_lines = body.splitlines()

    headings = []  # (0-based body index, normalized name)
    for idx, line in enumerate(body_lines):
        m = HEADING_RX.match(line)
        if m:
            headings.append((idx, m.group(1).strip().rstrip("#").strip().lower()))

    ass_start = next((i for i, n in headings if n == "assumptions"), None)
    where = rel(ws, run_dir)
    if ass_start is None:
        return False, ("%s:%d '## Assumptions' heading not found (searched "
                       "'^## ' headings)" % (where, offset + 1))
    ass_end = next((i for i, n in headings if i > ass_start), len(body_lines))
    ass_heading_line = offset + ass_start + 1

    body_dag, ass_dag = [], []
    for idx, line in enumerate(body_lines):
        if DAGGER not in line:
            continue
        if ass_start <= idx < ass_end:
            ass_dag.append((offset + idx + 1, line))
        else:
            body_dag.append((offset + idx + 1, line))

    if not body_dag:
        return True, ("%s:%d no '%s' markers outside the Assumptions section "
                      "(searched the whole body for '%s') - nothing to resolve"
                      % (where, offset + 1, DAGGER, DAGGER))
    if len(ass_dag) >= len(body_dag):
        return True, ("%s:%d Assumptions section carries %d '%s' line(s) "
                      "resolving %d body marker(s)"
                      % (where, ass_heading_line, len(ass_dag), DAGGER,
                         len(body_dag)))
    lineno, line = body_dag[len(ass_dag)]
    quote = line.strip()[:120]
    return False, ('%s:%d: "%s" - %d body marker(s) vs only %d line(s) under '
                   "'## Assumptions' (section at line %d); no matching "
                   "Assumptions entry for this marker"
                   % (where, lineno, quote, len(body_dag), len(ass_dag),
                      ass_heading_line))


# ---------------------------------------------------------------------------
# Assertions 5-6 - against outputs/questions.md
# ---------------------------------------------------------------------------

def read_questions(run_dir):
    """Return (text, lines) or (None, None) if outputs/questions.md is absent."""
    path = run_dir / "outputs" / "questions.md"
    if not path.is_file():
        return None, None
    text = path.read_text(encoding="utf-8", errors="replace")
    return text, text.splitlines()


QUESTIONS_MISSING = ("outputs/questions.md not found (searched that exact path "
                     "under the run dir)")


def check_5(run_dir):
    text, lines = read_questions(run_dir)
    if lines is None:
        return False, (QUESTIONS_MISSING + " - cannot confirm <=5 rounds or "
                       "Round 4 single-select")

    marks = []  # (1-based line, round number)
    for i, line in enumerate(lines, start=1):
        for m in ROUND_RX.finditer(line):
            marks.append((i, int(m.group(1))))

    if not marks:
        return False, ("outputs/questions.md:1 no round markers in %d lines "
                       "(searched case-insensitive regex 'round [#:-]? N') - "
                       "<=5 rounds cannot be confirmed" % len(lines))

    nums = sorted({n for _, n in marks})
    count = max(nums)
    max_line = max(i for i, n in marks if n == count)
    part1 = count <= 5
    e1 = ("outputs/questions.md:%d rounds recorded: %s - max %d, cap 5: %s"
          % (max_line, nums, count, "within cap" if part1 else "EXCEEDS cap"))

    r4 = next((i for i, n in marks if n == 4), None)
    if r4 is None:
        e2 = ("outputs/questions.md:%d no 'Round 4' marker found (rounds "
              "recorded: %s) - Round 4 single-select cannot be confirmed"
              % (marks[0][0], nums))
        return False, e1 + " | " + e2

    end_line = len(lines)
    for i, n in marks:
        if i > r4 and n > 4:
            end_line = i - 1
            break
    block = lines[r4 - 1:end_line]

    hits = []
    for j, line in enumerate(block):
        m = MULTI_RX.search(line)
        if m:
            hits.append((r4 + j, line.strip()[:120], m.group(0)))
    part2 = not hits
    if part2:
        e2 = ("outputs/questions.md:%d Round 4 block (lines %d-%d): no "
              "multi-select indicators (searched: multi-select, select/choose "
              "all, all of the above, select/choose multiple, more than one "
              "option, any number of)" % (r4, r4, end_line))
    else:
        first = hits[0]
        e2 = ('outputs/questions.md:%d: "%s" - Round 4 block (lines %d-%d) shows '
              "multi-select phrasing %r" % (first[0], first[1], r4, end_line,
                                            first[2]))

    return part1 and part2, e1 + " | " + e2


def check_6(run_dir):
    text, lines = read_questions(run_dir)
    if lines is None:
        return False, (QUESTIONS_MISSING + " - cannot scan offered options for "
                       "'all fine' / 'didn't read this'")
    for i, line in enumerate(lines, start=1):
        m = BAD_OPTION_RX.search(line)
        if m:
            quote = line.strip()[:160]
            return False, ('outputs/questions.md:%d: "%s" - matches forbidden '
                           "option pattern %r (case-insensitive search for "
                           "'all fine' / \"didn't read this\")"
                           % (i, quote, m.group(0)))
    return True, ("outputs/questions.md (all %d lines): case-insensitive search "
                  "for \"all fine\" / \"didn't read this\" variants - 0 matches"
                  % len(lines))


def main(argv):
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        sys.stderr.write("usage: check_assertions.py <run_dir>\n")
        return 2
    run_dir = Path(argv[1]).expanduser()
    if not run_dir.is_dir():
        die("not a directory: %s" % run_dir)
    run_dir = run_dir.resolve()

    assertions = load_assertions()
    root, deep = find_worksheets(run_dir)
    ws = pick_worksheet(root, deep)

    checks = [
        check_1(run_dir, root, deep),
        check_2(run_dir, ws),
        check_3(run_dir, ws),
        check_4(run_dir, ws),
        check_5(run_dir),
        check_6(run_dir),
    ]

    expectations = [
        {"text": assertions[i], "passed": bool(passed), "evidence": evidence}
        for i, (passed, evidence) in enumerate(checks)
    ]
    json.dump({"expectations": expectations}, sys.stdout, ensure_ascii=False,
              indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
