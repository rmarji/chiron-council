---
title: Claude on the web or desktop
parent: Install
nav_order: 1
description: "Install Chiron on claude.ai or the Claude desktop app, no terminal needed."
---

# Claude on the web or desktop

No terminal, no Python. This works on claude.ai and in the Claude desktop app.

## Install

1. Open **Customize → Plugins → Add → Add marketplace → Add from a repository**.
2. Paste `rmarji/chiron-council` and confirm. Leave everything else as it is.
3. Find **Chiron** under **Compound Club** and click **Install**.
4. Start a new chat and type:

   ```
   /chiron:council relationship "we keep having the same fight about money"
   ```

You'll see Claude open a few files and run a couple of small steps. That's Chiron loading each advisor's notes. After a minute or two you get a short answer with sources, where the advisors disagree, and one thing to do this week.

## Good to know

- **It always uses the latest version.** The repository dialog has no branch field and follows the main branch. It syncs on its own.
- **Two Chirons in your plugin list?** Keep the one under **Compound Club**. Remove any copy under **Local uploads**: that's an older manual upload and it won't update.
- **Try plain words too.** "What would Munger say about this contract?" works as well as a command.

## Update

Nothing to do; it syncs. To force a refresh, remove the marketplace and add it again with the same steps.

## Remove

Open **Customize → Plugins**, remove **Chiron**, then remove the **Compound Club** marketplace.

Next: [your first council](quickstart.md).
