# Using Chiron in Cowork

Chiron runs in Cowork with the same commands you get in Claude Code, but Cowork's sandbox handles files differently. This page covers installing in Cowork, where a distilled seat is allowed to land, and the two caveats that actually change how you work: a fixed model, and a one-click floor for delivering a new seat.

Cowork and Claude Code share the plugin format, so everything in [./installation.md](./installation.md) about the plugin applies. What is different is the sandbox, and it is worth understanding before you distill your first seat.

## Install Chiron in Cowork

Claude Code installs from a marketplace slug. Cowork installs from a file you accept in the app.

1. Download the `chiron.plugin` bundle from the latest release: `https://github.com/rmarji/chiron-council/releases/latest`
2. Open it in Cowork and accept it when the app asks you to trust the plugin.

If the download does not hand off to Cowork automatically, use the in-app fallback: **Extensions > Plugins > Upload**, then pick the `chiron.plugin` file you downloaded.

Trusting the plugin is what registers the seats and the `/chiron:*` commands. It is a one-time accept.

Once it is in, onboarding is identical to Claude Code:

```
/chiron:onboard
```

or jump straight to a real question:

```
/chiron:consult "take the retainer at 15k/mo or walk?"
/chiron:council relationship "we keep having the same fight about money"
```

## The sandbox reality

Here is the one fact that shapes everything downstream: **Cowork cannot write to your home directory.** In Claude Code, Chiron writes a distilled seat to `~/.claude/skills/<id>/` and it auto-activates on the next turn. Cowork has no such access, so `~/.claude/skills` and `~/.claude/chiron/seats` are off-limits mid-session. A distilled advisor cannot land in `~/.claude/skills` in Cowork, full stop.

That does not break Chiron. The registry scans several directories and merges them (project shadows global shadows bundled), and two of those scanned locations are writable from inside a Cowork workspace:

- **The workspace itself**, at `<project>/.chiron/seats/<id>/`. The registry scans `.chiron/seats`, so a seat written here is picked up by every council with no home-directory write and no extra step. It lives with that one workspace.
- **A `.plugin` bundle** you accept in-app, exactly like the Chiron install above. This one is portable across workspaces, but it costs one accept click.

So the sanctioned homes for a seat in Cowork are the workspace `.chiron/seats/` folder, or a `.plugin` you accept. Not `~/.claude`.

## Distilling a seat in Cowork

`/chiron:distill` runs the same flow described in [./distilling.md](./distilling.md): interview, deep research, author the full cited seat, then lint. Only the final delivery step changes, because of the sandbox.

- **If a workspace is open**, the seat is written to `<project>/.chiron/seats/<id>/`. The registry scans it, so it activates for councils in that workspace right away. No manual move, no accept click.
- **If there is no writable workspace**, Chiron emits a one-advisor `.plugin` into `outputs/`. You accept it in the app the same way you accepted Chiron, and then it is available across workspaces.

Contrast with Claude Code, where the same command writes `~/.claude/skills/<id>/` and the seat is global with zero extra clicks. In Cowork you either take a workspace-scoped seat for free, or you pay one accept click for a portable bundle.

## Distilling yourself in Cowork

`/chiron:distill-me` builds your private `me` seat: your mission, values, goals, frameworks, and the experts you already reach for. In Claude Code it writes `~/.claude/chiron/seats/me/`. In Cowork, with no home write, it writes the workspace path `<project>/.chiron/seats/me/`, which the registry scans.

The privacy rules are unchanged. Your `me` seat is private and local, never committed, never shipped. Because it lands inside the workspace in Cowork, add `.chiron/seats/` to that project's `.gitignore` so it never gets committed. Chiron offers to do this for you.

One consequence to plan around: a `me` seat distilled in one Cowork workspace lives in that workspace. It does not follow you to a different project the way a `~/.claude` seat would in Claude Code. If you want it everywhere, distill it into a `.plugin` and accept that, or redistill it per workspace.

## The one-accept-click floor

Be clear-eyed about this: in Cowork there is no path that is both zero-click and available everywhere. Claude Code gives you that; Cowork does not, and the reason is the sandbox, not Chiron.

| Harness | Where a distilled seat lands | Extra clicks | Scope |
|---|---|---|---|
| Claude Code | `~/.claude/skills/<id>/` | none | every project |
| Cowork (workspace) | `<project>/.chiron/seats/<id>/` | none | that workspace only |
| Cowork (portable) | `.plugin` accepted in-app | one accept | every workspace |

The workspace path is the cheapest option and it is genuinely zero-click, but it confines the seat to one project. The moment you want a seat to travel, you pay one accept click. Know that before you assume a seat you built in one workspace will show up in the next.

## The fixed-model caveat

Cowork runs a single, fixed model for the whole session. Claude Code lets you switch models, and that matters for Chiron in one specific way. Distilling and councils have a natural split between slow, careful work (planning the research, authoring a seat, synthesizing a council) and faster execution. In Claude Code you can point a stronger model at the thinking and a faster one at the execution. In Cowork you get one model for both.

In practice, a deep `/chiron:distill` or a large `/chiron:council` runs entirely on whatever model Cowork is set to. The output is the same shape and passes the same linter; you just do not get to tune the model per phase. For everyday consults this is a non-issue. For a heavy distill of a dense corpus, it is the main reason the same job can feel different across the two harnesses.

## Deep research in Cowork

The deep-research phase of `/chiron:distill`, surveying a subject's published corpus and extracting frameworks, heuristics, and citations into the reference files, runs inside Cowork's sandbox. The work and the depth bar are the same: real-person seats still carry 6,000 to 10,000 words of source-attributed references, and the linter still hard-fails a thin one.

Two honest differences from Claude Code:

- The research runs on the one fixed model, per the caveat above, so you cannot dedicate a stronger model to the extraction pass.
- The finished seat lands in the workspace or a `.plugin`, not in `~/.claude`, per the sandbox reality above.

Neither changes what a seat is. It changes where it lives and which model built it.

## What behaves the same

Once a seat is installed, the rest is identical to Claude Code. Seats auto-activate as native skills. `/chiron:consult` auto-routes, `/chiron:council` convenes seats and preserves dissent, benches are plain YAML, and per-seat memory works the same. Everything is still files: no server, no API keys.

If a seat you distilled does not show up, or a council cannot find it, start with [./troubleshooting.md](./troubleshooting.md). The usual cause in Cowork is a seat written outside a scanned directory, which the sandbox notes above are meant to head off.
