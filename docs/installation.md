# Installation

This page gets Chiron installed and verified. There are three paths: the full plugin in Claude Code, the same plugin in Cowork, and seats-only into any other agent via the `skills` CLI. Pick the one that matches where you work, then run the verify step at the bottom to confirm it took.

Chiron is all files. No server, no database, no API keys, MIT licensed. Installing it copies text into a skills directory and, for the plugin, registers ten slash commands.

## Prerequisites

- **A host that runs it.** The full plugin (orchestrator, live councils, benches, per-seat memory) needs **Claude Code** or **Cowork**, which share the plugin format. Seats alone run in any of the 70+ agents the `skills` CLI supports (Cursor, Codex, Gemini CLI, Copilot, Cline, and more).
- **Python 3.** The registry and linter (`scripts/registry.py`, `scripts/lint_seat.py`) are stdlib-only Python 3, and the slash commands shell out to them. macOS and most Linux boxes already have `python3`. Check with `python3 --version`.
- **Node / npx**, only for the seats-only path (`npx skills add ...`). Nothing else uses it.
- **Network access** for the initial install (marketplace fetch, release download, or `npx`) and for `/chiron:distill`, which does live web research. Everything else runs offline.

You do not need to clone the repo. The commands below pull from GitHub.

## Path 1: Claude Code plugin (recommended)

Two commands. Add the marketplace, then install the plugin from it:

```
/plugin marketplace add rmarji/chiron-council
/plugin install chiron
```

`rmarji/chiron-council` is the GitHub `owner/repo`; the plugin's own name is `chiron`, which is why the install line and every command are prefixed `chiron:`. After install, restart or reload if Claude Code prompts you to, then run onboarding or jump straight in:

```
/chiron:onboard
```

```
/chiron:consult "take the retainer at 15k/mo or walk?"
/chiron:council relationship "we keep having the same fight about money"
```

This path gives you the whole thing: `/chiron:consult` auto-routing, live councils, benches, and per-seat memory, plus all 18 bundled seats auto-activating as native skills.

## Path 2: Cowork

Cowork uses the same plugin format as Claude Code but installs from a file instead of a marketplace.

1. Download **`chiron.plugin`** from the latest release: [github.com/rmarji/chiron-council/releases/latest](https://github.com/rmarji/chiron-council/releases/latest).
2. Open it in Cowork and accept it. When prompted, **trust the plugin** (it is the only way its commands and seats load).
3. If the normal open-and-accept flow does not pick it up, install it manually: **Extensions > Plugins > Upload**, then select the `chiron.plugin` file.

Once accepted you get the same commands as Claude Code (`/chiron:consult`, `/chiron:council`, `/chiron:onboard`, and the rest). See [./cowork.md](./cowork.md) for the one real difference that matters: Cowork's sandbox cannot write to your home directory, so seats you distill and your private `me` seat land in the workspace at `.chiron/seats/` instead of `~/.claude/`.

## Path 3: Any agent via the skills CLI

Every seat is a standard [Agent Skill](https://agentskills.io), so the [`skills`](https://skills.sh) CLI drops the roster into any supported harness. This installs the seats, not the plugin: you get authored, cited advisors that auto-activate, but not the slash commands or the live-council orchestration (those are Claude Code and Cowork only).

```bash
npx skills add rmarji/chiron-council                                   # choose seats interactively
npx skills add rmarji/chiron-council --all                             # install the whole roster
npx skills add rmarji/chiron-council -a codex -s munger naval taleb    # one harness, a chosen subset
```

- **No flags:** interactive picker. It asks which agent and which seats.
- **`--all`:** installs every seat without prompting.
- **`-a <agent>`:** target a specific harness (`codex`, `cursor`, `gemini-cli`, and others).
- **`-s <seat...>`:** install only the named seats. Combine with `-a` for a scripted, one-line setup.

Outside the plugin you invoke a seat by talking to it, since there are no slash commands: "what would the Munger corpus say about this?" or "run this by Naval and Taleb." The seat activates like any other skill.

You can also copy a seat by hand into any agent's skills directory. That, plus the underlying skill format, is covered in [./portability.md](./portability.md).

## Verify the install worked

Two quick checks. First, list the roster:

```
/chiron:roster
```

You should see the seats grouped by domain, each showing `id · display_name · mode · domains · lint status`. All 18 bundled seats read `lint:pass`. If you get an error about no seats directory, the plugin did not load; see [./troubleshooting.md](./troubleshooting.md).

Then run a real routing decision through the orchestrator:

```
/chiron:consult "should I rewrite the landing page headline or leave it?"
```

Chiron states its verdict before it does anything ("this is a reversible copy tweak, so no council needed, routing to Voss alone"), which confirms both the commands and the seat loading are working. A council convening when it should not is the failure mode the orchestrator is built to avoid, so a clean SKIP or single-seat ASK here is the tool working, not a bug.

On the **seats-only path** there is no `/chiron:roster`. Verify by checking your agent's skills directory for the seat folders (for example `ls ~/.claude/skills` after a Claude Code install), or just ask a seat a question and confirm it answers in the cited, third-person corpus voice.

## Where the files live

Nothing is hidden. Chiron reads seats from several directories and merges them, with more specific scopes shadowing more general ones (project shadows global shadows bundled). The registry scans these paths in that precedence order:

| Location | What lives there | Scope |
|---|---|---|
| Plugin cache, e.g. `~/.claude/plugins/...` (the commands reach it as `${CLAUDE_PLUGIN_ROOT}/skills`) | The 18 bundled seats and the scripts. Do not edit these by hand. | Bundled |
| `~/.claude/skills/<id>/` | Seats you install with `npx skills` or distill in Claude Code. Auto-activate globally. | Global |
| `~/.claude/chiron/seats/<id>/` | Your private `me` seat and any personal seats. Gitignored, never shipped. | Global, private |
| `~/.claude/chiron/benches.yaml` | Your global benches (curated line-ups). Plain YAML. | Global |
| `<project>/.claude/skills/<id>/` | Project-scoped seats. | Project |
| `<project>/.chiron/seats/<id>/` | Project-scoped `me` seat and distilled seats. In Cowork, this is where everything you create lands. | Project |
| `<project>/.chiron/benches.yaml` | Project benches. Shadow global benches on a name collision. | Project |

The registry picks seats out of a shared skills root (`~/.claude/skills` can hold plenty of unrelated skills) by looking for the `x-chiron` marker in each `SKILL.md`. Unrelated skills and the Chiron router are ignored, so a busy skills directory does not confuse the roster.

Your `me` seat is deliberately private: it holds your mission, values, goals, and decisions, lives under `~/.claude/chiron/seats/` or a project's `.chiron/seats/`, is gitignored, and never gets committed or shipped from this repo. More on that in [./distilling.md](./distilling.md).

## Updating

- **Claude Code plugin:** refresh the marketplace, then update the plugin.

  ```
  /plugin marketplace update compound-club
  /plugin update chiron
  ```

  `compound-club` is the marketplace name (the repo can host more than one plugin under it); `chiron` is the plugin. If you are not sure of the marketplace name, `/plugin marketplace update` with no argument refreshes all of them.

- **Cowork:** re-download `chiron.plugin` from the [latest release](https://github.com/rmarji/chiron-council/releases/latest) and accept it again. The new version replaces the old.

- **Seats-only:** re-run the same `npx skills add` command you used. It pulls the current seats and overwrites them in place.

Updating the plugin or re-running `npx skills` only touches the bundled and installed seats. Your `me` seat, your distilled seats, your benches, and each seat's `log.md` live in separate directories and are left alone.

## Uninstalling

- **Claude Code plugin:**

  ```
  /plugin uninstall chiron
  /plugin marketplace remove compound-club
  ```

- **Cowork:** remove the Chiron plugin from **Extensions > Plugins**.

- **Seats-only:** delete the seat folders from your agent's skills directory, for example `rm -rf ~/.claude/skills/munger` (or whichever seats you added).

Uninstalling does not delete your personal data. If you want that gone too, remove `~/.claude/chiron/` (your `me` seat, personal seats, and global benches) and any project `.chiron/` directories yourself. That is your call to make, so Chiron never touches those on uninstall.

## Install troubleshooting

The common install failures and their fixes live in [./troubleshooting.md](./troubleshooting.md). The ones people hit most:

- **Plugin not showing after `/plugin marketplace add`:** the marketplace fetch or reload did not complete. Re-run the add, reload Claude Code.
- **Seats not appearing in the roster:** the plugin loaded but the skills root was not scanned, or a seat is failing lint (`lint:fail` seats will not load). Run `/chiron:lint <id> --explain`.
- **Cowork sandbox errors writing seats:** expected. Cowork cannot write to `~/.claude`; distilled and `me` seats go to the workspace `.chiron/seats/`. See [./cowork.md](./cowork.md).

## Next steps

- [./quickstart.md](./quickstart.md): your first consult, ask, and council in five minutes.
- [./concepts.md](./concepts.md): what a seat, a bench, and a council actually are.
- [./distilling.md](./distilling.md): add your own advisors and put yourself in the room.
- [../README.md](../README.md), [../SEAT_SPEC.md](../SEAT_SPEC.md), [../LEGAL.md](../LEGAL.md): the overview, the seat standard, and the provenance policy.
