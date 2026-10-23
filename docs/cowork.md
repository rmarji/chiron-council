---
title: Cowork
parent: Install
nav_order: 3
description: "Install Chiron in Claude Desktop's Cowork mode, and what its sandbox changes."
---

# Claude Desktop Cowork

Cowork installs plugins from a file instead of a marketplace.

## Install

1. Download **`chiron.plugin`** from the [latest release](https://github.com/rmarji/chiron-council/releases/latest).
2. Open it and click **Trust**. Chiron's commands and advisors only load once you trust it.
3. If nothing happens, go to **Extensions → Plugins → Upload** and pick the same file.
4. Start a task and type:

   ```
   /chiron:council relationship "we keep having the same fight about money"
   ```

Check the version in the release title. The file is built when a release is cut, so it can be a little behind the main branch. 0.3.0 and later include the ready-made councils.

## What's different in Cowork

Cowork runs in a sandbox that can't write to your home folder. Chiron works around that by saving everything in the open workspace instead of `~/.chiron/`:

| What | In Claude Code | In Cowork |
|---|---|---|
| Notes from past questions | `~/.chiron/logs/<advisor>/log.md` | `.chiron/logs/<advisor>/log.md` in the workspace |
| Your saved councils | `~/.chiron/benches.yaml` | `.chiron/benches.yaml` in the workspace |
| Advisors you build | `~/.chiron/seats/<id>/` | `.chiron/seats/<id>/` in the workspace |

So your history and any advisor you build stay with that workspace. They won't follow you to a different one.

If no workspace is open when you [build an advisor](distilling.md), Chiron packages it as a small `.plugin` file in `outputs/` instead. Open that file and click **Trust**, the same way you installed Chiron, and the advisor is available in every workspace. Downloading the file isn't enough on its own; it has to be trusted.

If you keep the workspace in git, add `.chiron/` to its `.gitignore` so your notes are never committed. Chiron offers to do this when it first writes there.

## Model choice

Cowork uses one model for the whole session. Councils and building a new advisor are the heaviest jobs, so if an answer comes back thin or the advisors blur together, switch to the strongest model Cowork offers and ask again.

## Update

Download the new `chiron.plugin` from the [latest release](https://github.com/rmarji/chiron-council/releases/latest) and open it. It replaces the old version.

## Remove

Remove Chiron from **Extensions → Plugins**. Delete the workspace's `.chiron/` folder if you want its notes gone.

Next: [your first council](quickstart.md).
