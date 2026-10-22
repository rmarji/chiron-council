# Chiron documentation

Chiron is an authored council of real thinkers for Claude Code, Cowork, ChatGPT, and Codex: cited, lint-enforced seats that disagree, not generated personas. These guides take you from install to getting real work out of it.

## Start here

- **[Installation](./installation.md)** - Prerequisites, the four ways to install (Claude Code, Cowork, ChatGPT and Codex, seats-only via `npx skills`), how to check it worked, where files live, updating, and uninstalling.
- **[Quickstart](./quickstart.md)** - From installed to your first sourced decision, either guided with `/chiron:onboard` or fast with `/chiron:consult`. Includes a full council run so you know what the output looks like.

## Guides

- **[Core concepts](./concepts.md)** - What a seat is, the three seat modes and why living people are corpus-only, per-seat memory, how `/chiron:consult` routes, how a council keeps takes independent, and benches.
- **[Commands reference](./commands.md)** - All eleven `/chiron:` commands with syntax, examples, guards, and when to reach for each.
- **[Distilling seats (and yourself)](./distilling.md)** - Add an advisor with `/chiron:distill`, or build your private `me` seat with `/chiron:distill-me`.
- **[Benches](./benches.md)** - Named line-ups you convene as a group: the YAML, where it lives, the bundled examples, and how big a bench should be.
- **[The seat standard](./the-standard.md)** - What makes a seat a seat, and how SEAT_SPEC, the linter, and the registry enforce it.
- **[Portability](./portability.md)** - Seats are standard Agent Skills, so they run in Cursor, Codex, Gemini CLI, and other agents. Councils, benches, and memory ship with the plugin (slash commands in Claude Code and Cowork; skills in ChatGPT and Codex).
- **[Using Chiron in Cowork](./cowork.md)** - Installing in Cowork, and how its sandbox changes where your seats get written.
- **[Getting the most out of Chiron](./getting-the-most.md)** - Routing by stakes, building benches you will reuse, distilling the minds you already reach for, and closing open loops.
- **[Why Chiron](./why-chiron.md)** - The case for authored seats over generated personas, and how Chiron answers the usual ways AI councils fail.
- **[Troubleshooting and FAQ](./troubleshooting.md)** - Seats not activating, "no seats found", lint failures, install errors, and common questions.

See also the [README](../README.md) for the short version, [CONTRIBUTING.md](../CONTRIBUTING.md) for running the linter and tests, [SEAT_SPEC.md](../SEAT_SPEC.md) for the full standard, and [LEGAL.md](../LEGAL.md) for provenance and the takedown policy.
