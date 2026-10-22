# Changelog

## 0.3.0 (2026-10-22)

- **Friendlier first run.** README has an "Install in 60 seconds" section for claude.ai, Claude Code, Claude Desktop/Cowork, Codex and ChatGPT, each with a first council to try. Plugin listings use plain words and a sample prompt.
- **Answers read like a person wrote them.** New `skills/chiron/VOICE.md`: plain labels, jargon explained, one clear next step, and a heads-up that a council takes 1–3 minutes.
- **Personal bits are opt-in.** Vault and `me.md` memory are offered, not assumed. The example `money` bench is now Munger, Naval and Hormozi; `deals` is Voss, Munger and Cialdini.
- **Fixes:** `/chiron:bench` asks before copying the example benches; `/chiron:log --open-loops` creates `~/.chiron` first and reads legacy logs without a contradiction.
- **Ferriss seat** (`tim-ferriss`, corpus mode) and the `work-design` example bench: Ferriss, Hormozi, Naval. The roster is now 19 seats.
- **`/chiron:coach`**: a guided decision session that frames the real call, consults seats as evidence, and ends on one committed, logged decision.
- **Example benches work out of the box.** With no benches file of your own, commands fall back to the bundled `benches/examples/benches.yaml`, so `/chiron:council relationship "..."` works on a fresh install. Your own benches file replaces the examples. New `scripts/benches.py` resolves which benches are in effect.
- **CI**: GitHub Actions lints every seat and runs the unit tests on Python 3.9 and 3.12. It also builds `chiron.plugin` and uploads it as an artifact. Cutting a GitHub release is still a manual step.
- **Consult logs, global benches, and seats Chiron writes** live under `~/.chiron/` (`CHIRON_HOME` overrides that directory; an explicit `--home` overrides the variable; Cowork passes `--home .chiron` because it cannot write the home directory). Claude Code refuses writes under `~/.claude`, so nothing is written there. Logs from `~/.claude/chiron/` are still read, and the next consult copies a seat's log into the new path.
- **Rayo OS** is described as Raed Marji's operating system, which a user can borrow. It is not the reader's.
- **Cowork bundle**: `python3 scripts/build_bundle.py dist/chiron.plugin` builds the `.plugin` file from the repo at the current `plugin.json` version.
- **Docs**: README rewritten around a quickstart; positioning moved to `docs/why-chiron.md`; install commands use the qualified `chiron@compound-club` form; seat counts, bench examples, and the bench write target corrected across `docs/`; added `CONTRIBUTING.md`.
- **ChatGPT and Codex plugin.** The repo root `plugin.json` is a portable Agent Plugins manifest, and `.agents/plugins/marketplace.json` publishes `chiron` from the Compound Club marketplace (`source` path `./`, the repo itself). Seats stay the existing `skills/<id>/` files. `ask`, `council`, `coach`, and `log` are skills that follow the command files, because those hosts have no slash commands. User data stays in `~/.chiron`. `python3 scripts/validate_openai_plugin.py` checks the manifest and marketplace.

## 0.2.0 (2026-07-23)

Seats reorganized as native Agent Skills, the full `docs/` set, and a rewritten README. See the [v0.2.0 release](https://github.com/rmarji/chiron-council/releases/tag/v0.2.0).

## 0.1.0 (2026-07-07)

First release. See the [v0.1.0 release](https://github.com/rmarji/chiron-council/releases/tag/v0.1.0).
