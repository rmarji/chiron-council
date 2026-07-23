# Chiron documentation

Chiron is an authored council of real thinkers for Claude Code and Cowork: cited, lint-enforced seats that disagree, not generated personas. These guides take you from install to getting real work out of it.

## Start here

- **[Installation](./installation.md)** - Chiron v0.2.0 installation page covering prerequisites and the three install paths (Claude Code marketplace plugin, Cowork .plugin, npx skills CLI), plus verify, file locations, updating, uninstalling, and install troubleshooting.
- **[Quickstart](./quickstart.md)** - docs/quickstart.md: two paths (guided /chiron:onboard and fast /chiron:consult) from install to a first sourced decision, with a realistic single-seat consult, a realistic cross-domain council showing positions/confidence/citations/authored-disagreement/synthesis, and the three daily commands plus the natural-language path.

## Guides

- **[Core concepts](./concepts.md)** - The concepts page for Chiron docs: seat as one authored mind implemented as a native Agent Skill, the three modes (corpus/original/persona) and why living people are corpus-only, the depth bar, per-seat memory, the /chiron:consult router, how a council gathers isolated takes and surfaces authored disagreement, benches, and the authored-vs-generated wedge.</summary>
</invoke>
.
- **[Commands reference](./commands.md)** - The docs/commands.md page: a full reference for all ten /chiron: commands (onboard, consult, ask, council, bench, roster, distill, distill-me, lint, log), each with syntax, behavior, a real example, guards/error codes, and when to use it, plus a natural-language section, grounded in the repo command files, scripts, and SEAT_SPEC.
- **[Distilling seats (and yourself)](./distilling.md)** - docs/distilling.md: how to grow the Chiron roster with /chiron:distill (interview, deep research to the depth bar, author as an auto-activating skill, lint) and build your private me seat with /chiron:distill-me.
- **[Benches](./benches.md)** - docs/benches.md: what benches are, the seats/chairman/default_depth YAML, global vs project shadowing, /chiron:bench and by-hand editing, example line-ups (money, strategy, relationship, detectives), 2-8 sizing guidance, when a bench beats a single ask, and chairing with the me seat.
- **[The seat standard (SEAT_SPEC and the linter)](./the-standard.md)** - docs/the-standard.md: what makes a seat a seat and how SEAT_SPEC plus the stdlib linter and registry enforce it.
- **[Portability: seats in any agent](./portability.md)** - docs/portability.md: seats are standard Agent Skills that run in any harness; install via the skills CLI or by hand, seats are universal while slash commands/orchestrator/councils/memory are plugin-only (Claude Code and Cowork).
- **[Using Chiron in Cowork](./cowork.md)** - docs/cowork.md: installing Chiron in Cowork and how its sandbox changes seat delivery (no home-dir write; workspace .chiron/seats or a one-click .plugin), plus the fixed-model and deep-research caveats.
- **[Getting the most out of Chiron](./getting-the-most.md)** - Power-user guide to Chiron: routing decisions by stakes (skip/ask/small council), letting the orchestrator route, building repeat-use benches, distilling your own experts and a private me seat, using the log's open-loops view, and the honest anti-sycophancy frame.
- **[Troubleshooting and FAQ](./troubleshooting.md)** - docs/troubleshooting.md: fixes for seats not activating, "no seats found", Cowork sandbox/model, lint failures (L1/L4/L5/L12), living-person refusal, duplicate ids, marketplace/install errors, plus a FAQ.

See also the [README](../README.md) for the short version, [SEAT_SPEC.md](../SEAT_SPEC.md) for the full standard, and [LEGAL.md](../LEGAL.md) for provenance and the takedown policy.

