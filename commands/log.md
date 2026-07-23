---
description: Review a seat's consult memory and surface open loops
argument-hint: <seat-id> [--open-loops]
---

# /chiron:log — the memory ledger

The user asked: `$ARGUMENTS`

Read the seat's `log.md` — its directory is the `path` the registry returns for `<id>` (bundled seats resolve under `${CLAUDE_PLUGIN_ROOT}/skills/<id>/`). If it doesn't exist: "No consults recorded with this seat yet." and stop.

## Default view

Render entries newest-first: date, source (`ask` or `council:<bench>`), question, take (condensed to one line), decision. Reading NEVER mutates the log.

## --open-loops

Filter to entries whose Decision is still `open loop`, flag those **older than 14 days** prominently — these are decisions the user consulted on and never closed. Close with one line: "Close a loop by telling me the decision — I'll record it." If the user then supplies a decision for an entry, update ONLY that entry's `**Decision:**` line (this is the single permitted mutation; never rewrite takes or questions).

## Housekeeping

If the log exceeds 100 entries, offer once to compress the oldest entries into an `## Archive digest` block (a dated summary of themes + decisions), keeping the newest 50 intact. Only do it if the user says yes.
