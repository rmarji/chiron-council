# Changelog

## 0.3.0 (unreleased)

- **Ferriss seat** (`tim-ferriss`, corpus mode) and the `work-design` example bench: Ferriss, Hormozi, Naval. The roster is now 19 seats.
- **`/chiron:coach`**: a guided decision session that frames the real call, consults seats as evidence, and ends on one committed, logged decision.
- **Example benches work out of the box.** With no benches file of your own, commands fall back to the bundled `benches/examples/benches.yaml`, so `/chiron:council relationship "..."` works on a fresh install. Your own benches file replaces the examples. New `scripts/benches.py` resolves which benches are in effect.
- **CI**: GitHub Actions lints every seat and runs the unit tests on Python 3.9 and 3.12.
- **Docs**: README rewritten around a quickstart; positioning moved to `docs/why-chiron.md`; install commands use the qualified `chiron@compound-club` form; seat counts, bench examples, and the bench write target corrected across `docs/`; added `CONTRIBUTING.md`.

## 0.2.0 (2026-07-23)

Seats reorganized as native Agent Skills, the full `docs/` set, and a rewritten README. See the [v0.2.0 release](https://github.com/rmarji/chiron-council/releases/tag/v0.2.0).

## 0.1.0 (2026-07-07)

First release. See the [v0.1.0 release](https://github.com/rmarji/chiron-council/releases/tag/v0.1.0).
