---
title: Claude Code
parent: Install
nav_order: 2
description: "Install Chiron in Claude Code with two commands."
---

# Claude Code

You need macOS or Linux and Python 3.9+ (`python3 --version`).

## Install

Inside Claude Code:

```
/plugin marketplace add rmarji/chiron-council
/plugin install chiron@compound-club
```

Choose **user** scope when asked, so Chiron works in every project. Reload if Claude Code asks you to.

`compound-club` is the marketplace name and `chiron` is the plugin, which is why every command starts with `/chiron:`.

## First question

```
/chiron:council relationship "we keep having the same fight about money"
```

The first time, Claude Code asks whether it can run `python3`. Allow it. Those small scripts read Chiron's own files and add a short note to `~/.chiron/logs/<advisor>/log.md`, so the advisors remember what you discussed. They don't touch anything else.

Want a quick check instead? `/chiron:roster` lists all 19 advisors.

## Update

From your shell (outside a session):

```bash
claude plugin marketplace update compound-club
claude plugin update chiron@compound-club
```

## Remove

```
/plugin uninstall chiron@compound-club
/plugin marketplace remove compound-club
```

Your notes in `~/.chiron/` stay. Delete that folder if you want them gone.

Next: [your first council](quickstart.md).
