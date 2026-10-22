# Contributing

Chiron is all files: seats are Markdown, the scripts are stdlib-only Python 3.9+. There is nothing to install.

## Run the checks

The same two commands run in CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) on every push and pull request:

```bash
python3 scripts/lint_seat.py --all              # every bundled seat; exit 0 pass / 1 warns / 2 errors
python3 -m unittest discover -s tests -v        # linter, registry, and bench resolver tests
```

CI fails on lint warnings as well as errors, so a PR should leave every seat at `PASS`. To dig into one seat: `python3 scripts/lint_seat.py skills/<id> --explain`.

## Adding a seat

The bar is [SEAT_SPEC.md](SEAT_SPEC.md); [docs/the-standard.md](docs/the-standard.md) explains it in prose. In short, a new seat needs:

- **Corpus mode for any real person.** Third person about the published record, never first-person impersonation of someone living (lint L1, L7).
- **At least three provenance sources** in the frontmatter (L4), and a source on every substantive claim.
- **All seven reference files** at the depth bar (L12). Existing real-person seats carry roughly 6,000 to 8,500 words across them.
- **A `disagreements.md` only if there is a real, citable conflict** with an installed seat, both positions sourced. Never invent one; councils exist to avoid manufactured conflict.
- **A clean lint run** and passing tests.

`/chiron:distill` produces a seat to this bar inside Claude Code; review its citations before opening a PR. Seats of living people stay corpus-mode, and [LEGAL.md](LEGAL.md) covers provenance and takedowns.

## Other changes

- If you add or remove a seat, update the seat count in `README.md` (badge, intro, roster table) and the docs that mention it. `python3 scripts/lint_seat.py --all` reports the count. `ask`, `council`, `coach`, `log`, and the `chiron` router share `skills/` and are not seats.
- Keep README and docs claims true of the repo as it is: commands, bench names, and paths in examples should exist.
- Note user-visible changes in [CHANGELOG.md](CHANGELOG.md).

## Releasing

CI does not publish a release or a tag. It builds `chiron.plugin` and uploads it as the `chiron-plugin` artifact, so a maintainer can download the bundle a pull request produced.

To cut a release by hand:

1. Bump `.claude-plugin/plugin.json` and the portable root `plugin.json` to the same version, and add the entry in [CHANGELOG.md](CHANGELOG.md). `python3 scripts/validate_openai_plugin.py` fails if those versions differ. The bundle check expects the version in `.claude-plugin/plugin.json` to be `0.3.0` until `EXPECTED_VERSION` in `scripts/build_bundle.py` is updated.
2. Build and check the Cowork bundle:

   ```bash
   python3 scripts/build_bundle.py dist/chiron.plugin
   python3 scripts/build_bundle.py --check dist/chiron.plugin
   ```

3. Tag the commit and publish a GitHub release with `dist/chiron.plugin` attached. Cowork installs that file. The marketplace install tracks the branch and does not need the release.
