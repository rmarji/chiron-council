---
title: Install
nav_order: 3
has_children: true
description: "Pick the app you already use. Each setup takes about a minute."
---

# Install Chiron

Pick the app you already use. Each guide takes about a minute and ends with the same first question, so you can see it work.

| You use | Guide | You need |
|---|---|---|
| Claude on the web (claude.ai) or the Claude desktop app | [Claude on the web or desktop](setup-claude-web.md) | Nothing else |
| Claude Code in a terminal | [Claude Code](setup-claude-code.md) | Python 3.9+ |
| Claude Desktop's Cowork mode | [Cowork](cowork.md) | The `chiron.plugin` file from the latest release |
| Codex CLI | [Codex](setup-codex.md) | Codex CLI, Python 3.9+ |
| ChatGPT desktop app | [ChatGPT](setup-chatgpt.md) | Codex CLI once, for the install step |
| Cursor, Gemini CLI, Copilot and others | [Other agents](portability.md) | Node, for `npx skills` |

Not sure? Start with **Claude on the web**. It needs no terminal and updates itself.

## What you get

- **19 advisors**, each built from one thinker's books, essays or talks. See [the advisors](advisors.md).
- **Six ready-made councils** (`money`, `deals`, `strategy`, `relationship`, `shipping`, `work-design`) that work before you set anything up. See [councils](benches.md).
- **Four everyday flows:** ask one advisor, call a council, get coached to a decision, and look back at what you decided. In Claude these are `/chiron:` commands. In Codex and ChatGPT you ask in plain words.

## Requirements

- **macOS or Linux** for Claude Code, Cowork, Codex and ChatGPT. Windows isn't supported yet. WSL may work but hasn't been tested.
- **Python 3.9 or newer** on those same apps. Run `python3 --version` to check; macOS already has it. Nothing to `pip install`.
- **Claude on the web needs nothing.**
- **Internet** for the install itself and for [building a new advisor](distilling.md). Asking the advisors you have needs no extra network calls beyond the AI app you're using.

## After installing

1. Ask your first question. The [quickstart](quickstart.md) walks you through it.
2. Optional: run `/chiron:onboard` (or say "set up Chiron for me") for a five-minute setup that builds councils around what you're working on.

Your notes and councils live in `~/.chiron/` on your computer. [Your data and memory](your-data.md) explains what's saved.

## Update or remove

Each setup guide has its own update and uninstall steps. Removing Chiron never deletes `~/.chiron/`. Delete that folder yourself if you want your notes gone too.
