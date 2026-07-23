---
description: Validate seats against SEAT_SPEC — the standard, enforced
argument-hint: [seat-id | --all] [--strict] [--explain]
---

# /chiron:lint — enforce the seat standard

Run the linter (stdlib-only Python; CI runs the same file):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py --all --seats-dir ${CLAUDE_PLUGIN_ROOT}/skills
# or a single seat:
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/lint_seat.py ${CLAUDE_PLUGIN_ROOT}/skills/<id> [--level strict] [--explain]
```

Exit codes: 0 = pass, 1 = warnings only, 2 = errors (a failing seat will not load).

Report the results plainly. For each finding, show the rule id, what it means (the `--explain` flag prints rule descriptions; SEAT_SPEC.md §7 has the full table), and the concrete fix:

- **L1** persona+living+unlicensed → switch `mode: corpus` or adopt the archetype `alias` (see LEGAL.md). Non-negotiable.
- **L4** < 3 sources → add citations to `provenance.sources` (draw from `references/sources.md`).
- **L5** missing/thin sections → add Priors/Heuristics/Refusals/Voice entries per SEAT_SPEC §3.
- **L7** first-person leakage → rewrite to third-person analytic, or put subject speech in quotation marks.
- **L12** missing reference files → the seat shipped without its depth; author the missing files per SEAT_SPEC §4.

If the user asks you to fix findings, fix the mechanical ones (frontmatter, naming, voice rewrites) directly in the seat files and re-run until clean; content gaps (L5/L12) need real authoring — offer to do it at the SEAT_SPEC depth bar, not with filler.
