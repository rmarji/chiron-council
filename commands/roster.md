---
description: List installed seats — who is available to ask or bench
argument-hint: [--domain <tag>]
---

# /chiron:roster — who's available

Run:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/registry.py --seats-dir ${CLAUDE_PLUGIN_ROOT}/seats --seats-dir ~/.claude/chiron/seats --seats-dir .chiron/seats [--domain <tag>]
```

(Use `--json` if you need to post-process.)

Render the roster grouped by primary domain: **id · display_name · mode · domains · lint status**. Pass `--domain <tag>` through when the user gave one.

- If lint shows `warn`, add a one-line note; if `fail`, mark the seat unloadable and point to `/chiron:lint <id> --explain`.
- If the exit code is 2 (no seats directory): tell the user to run `/chiron:distill` or install a pack.
- At large rosters (dozens of seats), keep the grouped view — never dump every seat's details; summarize per domain and expand only the domain the user asked about.
- Close with a hint: `/chiron:ask <id> "<question>"` and `/chiron:bench create <name> <ids...>`.
