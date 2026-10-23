---
title: FAQ
nav_order: 9
description: "Short answers to the questions people ask most."
---

# FAQ

### What is Chiron, in one line?
A set of 19 advisors built from real thinkers' published work, plus a way to ask several of them the same question and see where they disagree.

### Which apps does it work in?
Claude on the web and desktop, Claude Desktop's Cowork mode, Claude Code, the Codex CLI, and the ChatGPT desktop app. The advisors on their own also work in Cursor, Gemini CLI, Copilot and other agents; see [other agents](portability.md).

### Does it cost anything?
No. It's MIT licensed and needs no API key. You use whatever AI plan you already have.

### Is it really Munger talking?
No. Each advisor reports what the thinker's books, essays and talks say, with the source, and talks *about* them ("Munger's writing says…"). It never pretends to be the person, and no thinker has endorsed it.

### Why do I sometimes get one advisor instead of a council?
Because the question didn't need more. A small choice you can easily undo gets one advisor or a direct answer. A council is for expensive, hard-to-undo or many-sided decisions. If you want a council anyway, say "make it a full council" or call one by name: `/chiron:council money "…"`.

### The advisors didn't disagree. Is that broken?
No. Chiron only shows disagreements that are on record in the thinkers' work. If there isn't one for your question, it says so instead of inventing an argument.

### How long does a council take?
One to three minutes. You'll see the app open a few files and run a couple of small scripts first. That's Chiron loading each advisor's notes.

### What does it save, and where?
Short notes in `~/.chiron/` on your computer, and only what you asked and decided. Nothing goes anywhere except the AI app you're using. See [your data and memory](your-data.md).

### Does it read my personal notes or files?
Not unless you build a personal advisor with `/chiron:distill-me`, which asks before reading each source.

### Why don't `/chiron:` commands work in Codex or ChatGPT?
Those apps don't have slash commands. Ask in plain words instead: "Convene the money council: …" or "Ask Voss how to answer this counteroffer."

### Can I add my own advisor?
Yes. `/chiron:distill "Ray Dalio's Principles"` researches the person's published work and builds one with sources. You can also build one of yourself. See [Build an advisor](distilling.md).

### Can I make my own councils?
Yes. Say "make me a council called hiring with Munger and Voss", or use `/chiron:bench create`. See [councils](benches.md).

### Does it work offline?
Chiron needs no server of its own, but your AI app needs its normal connection. Building a new advisor also does web research.

### Does it work on Windows?
Not yet. WSL may work but hasn't been tested. Claude on the web works from any computer.

### Who's Rayo OS?
The Chiron author's own decision rules, included as an example of an advisor built from your own principles. It only sits on the `shipping` council.

### How do I update?
Claude on the web updates itself. For the other apps, see the update steps in each [setup guide](installation.md).

### Something's not working.
See [troubleshooting](troubleshooting.md), or [open an issue](https://github.com/rmarji/chiron-council/issues).
