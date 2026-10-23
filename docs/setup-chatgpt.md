---
title: ChatGPT
parent: Install
nav_order: 5
description: "Install Chiron in the ChatGPT desktop app."
---

# ChatGPT desktop app

ChatGPT reads plugins from the same place Codex does, so you need the Codex CLI once for the install step. You need macOS or Linux and Python 3.9+.

## Install

1. In a terminal:

   ```bash
   codex plugin marketplace add rmarji/chiron-council
   ```

2. **Quit and reopen ChatGPT.** It only reads new marketplaces at start-up, and this is the step people miss.
3. Turn on **Work** mode, open **Plugins**, choose **Compound Club**, and install **Chiron**.
4. In a new chat:

   > Convene the relationship council: we keep having the same fight about money.

ChatGPT has no slash commands. Ask in plain words, or type `@council`.

## Update

```bash
codex plugin marketplace upgrade compound-club
```

Then restart ChatGPT.

## Remove

Remove Chiron from **Plugins**, run `codex plugin marketplace remove compound-club`, and restart the app.

Next: [your first council](quickstart.md).
