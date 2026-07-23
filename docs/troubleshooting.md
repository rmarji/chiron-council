# Troubleshooting and FAQ

The common things that go wrong with Chiron, and the exact fix for each. If your problem is not here, run `/chiron:lint <id> --explain` for seat issues, or open an issue on the [repo](../README.md).

## A seat you distilled or copied is not activating

Symptom: you ran `/chiron:distill`, or copied a seat folder by hand, but Claude does not pick it up when the topic comes up, and it does not show in `/chiron:roster`.

Seats are native Agent Skills. The skills loader scans your skills directories when a session starts, so a seat written mid-session may not auto-activate until the loader rescans. Work through this in order:

1. **Confirm where it landed.** A seat must be a directory with a `SKILL.md` inside a scanned location. In Claude Code, `/chiron:distill` writes to `~/.claude/skills/<id>/` (global, auto-activating) or `<project>/.claude/skills/<id>/` (project-scoped). Check it is there:

   ```bash
   ls ~/.claude/skills/<id>/SKILL.md
   ```

2. **Confirm it has an `x-chiron` block.** The registry and the roster only count a skill as a seat if its `SKILL.md` frontmatter carries an `x-chiron:` block. A skill without it loads as a plain skill but never appears as a Chiron seat. Open the file and check the frontmatter has `x-chiron:` with a `display_name`, `mode`, and `domains`.

3. **Reload so the loader rescans.** Start a fresh Claude Code session (or reload the plugin) so the skills loader picks up the new `skills/<id>/` directory. A newly written skill will not always attach to the session that wrote it.

4. **Verify it is now in the roster:**

   ```
   /chiron:roster
   ```

   If it appears with `lint:pass`, it is live. If it shows `lint:warn` or `lint:fail`, see [Lint failures](#lint-failures-and-what-each-rule-means) below. A `fail` seat will not load.

### In Cowork it still will not activate

Cowork runs in a sandbox and **cannot write to `~/.claude`**. Two things follow:

- `/chiron:distill` and `/chiron:distill-me` write a seat into the open workspace at `<project>/.chiron/seats/<id>/` instead. The registry scans that path, so councils find it with no home directory write. Confirm the seat is under `.chiron/seats/` in your workspace, not somewhere the sandbox cannot reach.
- If there is no writable project, the distill flow emits a one-advisor `.plugin` into `outputs/`. That file does nothing until you **accept it in the app**. Downloading it is not installing it. Open it in Cowork and accept the install, the same accept step you did for `chiron.plugin` itself. See [cowork.md](./cowork.md) for the full sandbox model.

## "No seats found" from a command

Two different causes, and they have different fixes.

**Cause 1: no scanned directory exists at all.** `registry.py` exits with code 2 and prints `no seats directory found; run /chiron:distill or install a pack`. This means none of the scanned locations exist yet. The scanned set, lowest precedence to highest, is:

```
<plugin>/skills   ~/.claude/skills   ~/.claude/chiron/seats   .claude/skills   .chiron/seats
```

If you are running the plugin, the bundled `skills/` should always be present, so this error usually means you are running the raw scripts outside the plugin root. Run from the repo checkout, or point at a real directory:

```bash
python3 scripts/registry.py --seats-dir skills
```

**Cause 2: your seat is present but not in a scanned location, or has no `x-chiron` block.** The registry deliberately ignores any skill that lacks an `x-chiron:` marker, so a shared skills root full of unrelated skills (and the Chiron router itself) is safe to scan. If your seat sits in a directory that is not in the list above, or its frontmatter is missing the `x-chiron` block, it will be silently skipped, not errored. Fix: move it into a scanned dir (`~/.claude/skills/<id>/` is the usual one) and add the `x-chiron` block. Then `/chiron:roster` should list it.

To see exactly what the registry sees, run it directly with the full scan set:

```bash
python3 scripts/registry.py --json \
  --seats-dir skills \
  --seats-dir ~/.claude/skills \
  --seats-dir ~/.claude/chiron/seats \
  --seats-dir .claude/skills \
  --seats-dir .chiron/seats
```

## Model selection in Cowork

Councils and distills are heavier than a single ask: a council gathers several seats in isolation and then synthesizes, and `/chiron:distill` runs multiple rounds of deep research. If a council comes back shallow, truncated, or the seats blur together, check which model Cowork has selected and switch to the strongest one available before re-running. Chiron ships no model config of its own, no API keys, and no server, so model choice is entirely the host app's setting. See [cowork.md](./cowork.md).

## Lint failures and what each rule means

Run the linter on any seat to see why it will not load. Inside the plugin:

```
/chiron:lint <id> --explain
```

From a repo checkout:

```bash
python3 scripts/lint_seat.py skills/<id> --explain
python3 scripts/lint_seat.py --all              # every bundled seat
```

Exit codes: **0** pass, **1** warnings only, **2** errors. An exit-2 seat is load-blocking: it will not load until you fix the error. Warnings do not block loading but are worth clearing.

The load-blocking rules you will hit most:

| Rule | Level | Means | Fix |
|---|---|---|---|
| **L1** | error | `mode: persona` on a living subject with no granted license. Forbidden by [LEGAL.md](../LEGAL.md), non-negotiable. | Switch to `mode: corpus`, or use an original-mode archetype `alias`. See the next section. |
| **L4** | error | corpus or persona seat with fewer than 3 provenance sources. | Add citations to `provenance.sources` in the frontmatter, drawn from `references/sources.md`. Real-person seats ship five or more. |
| **L5** | error | A required section (`## Priors`, `## Heuristics`, `## Refusals`, `## Voice`) is missing or below its minimum entry count (Priors and Heuristics need 5 each, Refusals need 2). | Author the missing entries per [SEAT_SPEC §3](../SEAT_SPEC.md). Not filler: each prior must be specific enough to disagree with, each heuristic in IF/THEN shape. |
| **L12** | warn (error at `--level strict`) | `references/` is missing one or more of the 7 standard files (`principles.md`, `mental-models.md`, `frameworks.md`, `anti-patterns.md`, `heuristics.md`, `quotes.md`, `sources.md`). | The seat shipped without its depth. Author the missing files at the [SEAT_SPEC §4](../SEAT_SPEC.md) depth bar. This is the difference between a seat and a name. |

Warnings you may also see: **L6** (SKILL.md over ~6k tokens, move depth into `references/`), **L7** (first-person subject voice in a corpus seat, rewrite to third-person analytic or put subject speech in quotation marks; this becomes an error at `--level strict`), **L8** (a heuristic that is not in operational IF/THEN form), **L9** (a `disagreements.md` counterpart that names a seat you do not have installed and is not marked `external:`), and **L10** (the subject's name in `display_name` without a mode suffix like "Lens" or "(corpus)").

If you ask Claude to fix findings, it will fix the mechanical ones (frontmatter, naming, voice rewrites) directly. Content gaps (L5, L12) need real authoring at the depth bar, not padding. See [the-standard.md](./the-standard.md) for the full rule table.

## Chiron refused to impersonate a living person

If you asked to distill a living person in first-person "be them" voice and Chiron declined, that is by design, not a bug. Corpus mode is required for living, unlicensed subjects. The distill flow (CH-E8) and lint rule **L1** both hard-fail persona mode for a living person without a granted license, because of right-of-publicity and false-endorsement exposure documented in [LEGAL.md](../LEGAL.md).

You have two supported paths, and Chiron will offer both:

- **Corpus mode** (recommended): the seat speaks in the third person about the person's published work, cited per claim ("the Hormozi corpus would flag..."). This is what all 14 real-person founding seats use, and it is why sourced heuristics beat generated vibes.
- **An original-mode archetype alias**: an invented advisor like "The Offer Architect" instead of the named person, with no provenance constraints.

There is no phrasing that gets you living-person persona mode without a license. That is the guardrail working. See [distilling.md](./distilling.md).

## Two seats have the same id

This is expected and usually intentional: it is how you override a bundled seat with your own richer version. The registry resolves it by **precedence**, lowest to highest: bundled, then `~/.claude/skills/`, then `~/.claude/chiron/seats/`, then project `.claude/skills/`, then project `.chiron/seats/`. A later scope **shadows** an earlier one on a shared id, so your own `munger` in `~/.claude/skills/munger/` wins over the bundled `munger`. In the roster you will see the winning seat annotated with `(shadows <path>)`.

Two caveats:

- **Same id twice in one scope is an error, not an override.** If two folders in the *same* directory both declare `name: munger`, that is an ambiguous collision (lint **L3**), and the registry fails both. Rename one.
- **The native skill loader is not the registry.** Two seats named `munger` in different scanned dirs mean the skills loader also sees two skills called `munger`. The Chiron registry resolves the override cleanly, but if you notice the native loader behaving oddly around the duplicate, remove the copy you are not using rather than keeping both.

## Marketplace listing not appearing, or "cloud not linked" during install

Install issues live in [installation.md](./installation.md); the highlights:

- **The marketplace does not appear after `/plugin marketplace add`.** Confirm you ran `/plugin marketplace add rmarji/chiron-council` exactly (the marketplace repo slug), then `/plugin install chiron` (the plugin name is `chiron`, not the repo name). If the add succeeded but install cannot find `chiron`, re-run the add and reopen the plugin menu so the listing refreshes.
- **"Cloud not linked" or a sign-in prompt during install.** The plugin marketplace flow needs your Claude Code client linked to your account. This is a client and account state issue, not a Chiron issue: complete the link or sign-in the client asks for, then retry `/plugin install chiron`. Chiron itself needs no account, no keys, and no server.
- **In Cowork, there is no marketplace command.** You install by downloading [`chiron.plugin`](https://github.com/rmarji/chiron-council/releases/latest) from the latest release and accepting it in the app. See [cowork.md](./cowork.md).

## FAQ

**Is my `me` seat private?**
Yes. `/chiron:distill-me` writes an original-mode `me` seat to `~/.claude/chiron/seats/me/` (or `<project>/.chiron/seats/me/`). It holds your mission, values, goals, and decisions. It is never committed to the plugin repo and never shipped. If it is written into a project, add `.chiron/seats/` to that project's `.gitignore` (the flow offers to do this). Treat it like `log.md`: local, personal, yours.

**Does the per-seat memory get shared?**
No. Each seat's `log.md` is append-only, local, and gitignored by default. It holds your decisions, not the seat's content, so it stays on your machine.

**Does Chiron work offline?**
The seats do. Everything is files: no server, no API keys, no network calls to run a council or ask a seat. The one exception is `/chiron:distill`, which needs web access to do the deep research over a subject's published corpus. Distilling a new seat requires a connection; using the seats you already have does not.

**Which agents are supported?**
The plugin (slash commands, the `/chiron:consult` orchestrator, live councils, benches, per-seat memory) runs in Claude Code and Cowork. The seats themselves are standard Agent Skills and drop into 70+ harnesses (Cursor, Codex, Gemini CLI, Copilot, Cline, and more) via `npx skills add rmarji/chiron-council`, or by copying a seat folder into the agent's skills directory. Outside the plugin you invoke a seat by talking to it ("what would the Munger corpus say about this?"). Full detail in [portability.md](./portability.md).

**A council gave consensus with no disagreement. Is it broken?**
No. Councils surface **only** authored disagreements, conflicts pulled from what the people actually argued, both positions cited. If no authored disagreement exists between the seated experts on your topic, the council says so rather than inventing one. Manufactured conflict is the failure mode Chiron exists to avoid. See [concepts.md](./concepts.md).

**`/chiron:consult` said no council was needed. Did it fail?**
No. The orchestrator's most valuable verdict is often SKIP or a single ASK. A cheap, reversible call does not warrant a council, and convening one anyway is decision theater and a token tax. If you want a full council regardless, say "make it a full council" or name the bench directly with `/chiron:council <bench> <question>`. See [commands.md](./commands.md).
