---
title: Troubleshooting
nav_order: 10
description: "What to do when something's off."
---

# Troubleshooting

Find what you're seeing, then do what the right column says. If it's not here, [open an issue](https://github.com/rmarji/chiron-council/issues).

## Quick fixes

| What you see | What to do |
|---|---|
| Two Chiron plugins in Claude's list | Remove the one under **Local uploads**; keep **Compound Club**. |
| claude.ai has an older version | The repository dialog always follows the main branch. Remove the marketplace and add it again to refresh. |
| Codex doesn't know about Chiron | Start a new `codex` session. Plugins load when a session starts. |
| ChatGPT doesn't show Compound Club | Quit and reopen ChatGPT after `codex plugin marketplace add`. Then look under **Plugins** in **Work** mode. |
| `/chiron:...` does nothing in Codex or ChatGPT | Those apps don't have slash commands. Ask in plain words: "Convene the money council: …" |
| Codex saved notes in `.chiron/` inside your project | Its sandbox couldn't write to your home folder. That's fine. Approve the write to `~/.chiron` next time if you want one shared history. |
| Claude Code asks about `python3` | Allow it. The scripts read Chiron's files and add short notes under `~/.chiron/logs/`. |
| Claude Code keeps asking for permission | Allow each `python3` call. If it asks about other shell commands, tell Claude to "run each python3 call on its own"; Chiron's instructions already ask for this. |
| Cowork can't find the `relationship` council | Your `chiron.plugin` is older than 0.3.0. Download the [latest release](https://github.com/rmarji/chiron-council/releases/latest) and open it again. |
| Chiron can't find an advisor you named | Check the spelling with `/chiron:roster` (or "which Chiron advisors do I have?"). Ids are lowercase, like `terry-real` and `tim-ferriss`. |
| A council came back thin or the advisors sound alike | Switch your app to its strongest model and ask again. Councils are the heaviest thing Chiron does. |
| The advisors didn't disagree | That's expected when nothing is on record. Chiron doesn't invent arguments. |
| Chiron answered with one advisor, not a council | It judged the question small. Say "make it a full council" if you want more. |
| You're on Windows | Not supported yet. WSL may work but hasn't been tested. Claude on the web works anywhere. |

## Install problems

**Claude Code: Chiron doesn't appear after adding the marketplace.** Check you ran exactly `/plugin marketplace add rmarji/chiron-council`, then `/plugin install chiron@compound-club`. The plugin is `chiron` and the marketplace is `compound-club`; neither is the repo name. `/plugin marketplace list` should show `compound-club`.

**Claude Code: "cloud not linked" or a sign-in prompt.** That's your Claude Code account state, not Chiron. Finish the sign-in it asks for, then install again. Chiron itself needs no account or key.

**Codex: `codex plugin list` prints thousands of lines.** It lists the whole public catalogue. Use `codex plugin list | grep chiron`.

**Codex: don't use `--sparse`.** A sparse checkout of `.agents/plugins` leaves out the advisors.

## An advisor you built isn't showing up

1. **Check where it landed.** Chiron saves new advisors to `~/.chiron/seats/<id>/` (or `.chiron/seats/<id>/` in a project or Cowork workspace). Run `ls ~/.chiron/seats/<id>/SKILL.md`.
2. **Start a new session.** Apps scan for skills when a session starts.
3. **Run `/chiron:roster`.** If it's listed as `fail`, run `/chiron:lint <id> --explain` and see [the advisor standard](the-standard.md).

In Cowork, an advisor packaged as a `.plugin` file does nothing until you open it and click **Trust**. See [Cowork](cowork.md).

## Two advisors with the same name

That's how you replace a bundled advisor with your own version. Yours wins: `~/.chiron/seats/munger/` overrides the bundled `munger`, and a project's `.chiron/seats/munger/` overrides both. The roster marks the winner with `(shadows <path>)`.

Two folders with the same name in the *same* place is an error (lint rule L3). Rename one.

## Chiron wouldn't imitate a living person

By design. Advisors based on living people describe their published work in the third person, with sources. Chiron won't build a first-person "be them" version without a licence from the person; see [LEGAL.md](https://github.com/rmarji/chiron-council/blob/main/LEGAL.md). It offers two alternatives: a sourced advisor about the person, or an invented advisor with its own name ("The Offer Architect").

## For contributors: checking the registry by hand

From a repo checkout:

```bash
python3 scripts/registry.py --json --seats-dir skills --seats-dir ~/.chiron/seats
python3 scripts/lint_seat.py --all
python3 scripts/lint_seat.py skills/*        # flow skills are skipped
```

`registry.py` exits with code 2 and `no seats directory found` when none of the folders you passed exist. It scans these folders, lowest to highest priority:

```
<plugin>/skills  ~/.claude/skills  ~/.claude/chiron/seats  ~/.chiron/seats  .claude/skills  .chiron/seats
```

It only counts folders whose `SKILL.md` has an `x-chiron:` block, so unrelated skills in a shared folder are ignored. The `~/.claude` folders are read, never written.

Lint exit codes: `0` pass, `1` warnings, `2` errors (the advisor won't load). The full rule table is in [the advisor standard](the-standard.md).
