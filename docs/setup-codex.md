---
title: Codex
parent: Install
nav_order: 4
description: "Install Chiron in the Codex CLI."
---

# Codex

You need the Codex CLI, macOS or Linux, and Python 3.9+.

## Install

```bash
codex plugin marketplace add rmarji/chiron-council
codex plugin add chiron@compound-club
codex plugin list | grep chiron
```

The last line should say something like `chiron@compound-club  installed, enabled  0.3.0`. (Without the `grep`, `codex plugin list` prints the whole public catalogue, which is long.)

## First question

Open a **new** `codex` session. Plugins load when a session starts, so an open session won't see Chiron yet. Then type:

```
Convene the relationship council: we keep having the same fight about money.
```

Codex has no slash commands, so ask in plain words. "Ask Munger about this contract", "run this past the money council" and "coach me through this decision" all work. You can also type `@council`.

## Where your notes go

Normally in `~/.chiron/`. If Codex's sandbox won't let it write to your home folder, it saves them in a `.chiron/` folder inside the current project and tells you in one line. That's fine. If you'd rather keep one shared history, approve the write to `~/.chiron` next time Codex asks.

## Update

```bash
codex plugin marketplace upgrade compound-club
codex plugin add chiron@compound-club
```

## Remove

```bash
codex plugin remove chiron@compound-club
codex plugin marketplace remove compound-club
```

Next: [your first council](quickstart.md).
