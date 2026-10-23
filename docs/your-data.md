---
title: Your data and memory
nav_order: 7
description: "What Chiron saves, where it lives, and how to delete it."
---

# Your data and memory

Everything Chiron saves is a plain text file on your computer, in `~/.chiron/`. Nothing is sent anywhere except to the AI app you're already using. Delete the folder and Chiron forgets everything.

## What's saved

| File | What's in it | When it's written |
|---|---|---|
| `~/.chiron/logs/<advisor>/log.md` | A short note per question: the date, what you asked, the advisor's one-line take, and your decision (or "open loop" if you didn't say) | After each answer from that advisor |
| `~/.chiron/benches.yaml` | Councils you saved | When you create or edit a council |
| `~/.chiron/seats/<id>/` | Advisors you built, including your private `me` advisor if you made one | When you build an advisor |

Notes are added, never rewritten. The one exception: when you tell Chiron what you decided, it fills in the decision on that note.

## How memory works

When you ask an advisor again, it reads its last 10 notes, so it can say things like "In June you asked about the index position and decided to wait." That's the whole memory system.

Telling it your decision is optional. At the end of an answer you'll see:

> Want me to remember what you decide, so these advisors can follow up next time?

Answer with your decision and it's recorded. Ignore it and the note stays marked "open loop". Chiron won't ask again in the same session. `/chiron:log <advisor> --open-loops` shows the decisions you never closed.

## Nothing personal unless you set it up

Out of the box, Chiron doesn't read your notes app, your instruction files, or anything about you. A personal `me` advisor exists only if you build one with `/chiron:distill-me`, and that flow asks before reading each source. See [Build an advisor](distilling.md#your-own-advisor).

## Different apps, different places

- **Claude Code, Codex, ChatGPT:** `~/.chiron/`.
- **Codex inside a sandbox** that can't write to your home folder: a `.chiron/` folder in the current project. Codex tells you when it does this. Approve the write to `~/.chiron` next time if you want one shared history.
- **Cowork:** a `.chiron/` folder in the open workspace, because Cowork can't write to your home folder. See [Cowork](cowork.md).
- **Claude on the web:** Chiron runs inside Claude's own sandbox, so whether notes carry over between chats depends on that environment. Treat memory there as best-effort, and use Claude Code, Codex or ChatGPT if you want a lasting history on your own computer.

If you keep a project in git, add `.chiron/` to its `.gitignore`. Chiron offers to do this when it writes there.

## Change the location

Set `CHIRON_HOME` to use a different folder:

```bash
export CHIRON_HOME=~/Documents/chiron
```

## Older installs

Before 0.3.0, Chiron kept notes under `~/.claude/chiron/`. Those files are still read. The next time you ask an advisor, its old notes are copied into `~/.chiron/` and the old file is left alone. Once you've used each advisor, you can delete `~/.claude/chiron/`.

## Delete everything

```bash
rm -rf ~/.chiron
```

Also remove any `.chiron/` folders in projects or Cowork workspaces. Uninstalling the plugin doesn't delete these; that's your call.
