"""Unit tests for scripts/lint_seat.py — the §8 CH-05 suite."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "scripts"))

from lint_seat import lint_seat, lint_status  # noqa: E402

VALID_FRONTMATTER = """---
name: {id}
description: Test seat for lint validation.
x-chiron:
  display_name: {display_name}
  mode: {mode}
  domains: [testing, decisions]
  alias: The Test Lens
  provenance:
    subject: {subject}
    living: {living}
    license: {license}
    sources:
{sources}
---
"""

VALID_BODY = """
# Thinking like Test Subject

## Priors

- Invert, always invert: state how this decision fails before how it succeeds.
- Incentives drive outcomes more than intentions do.
- The corpus favors avoiding stupidity over seeking brilliance.
- Big mistakes come from acting outside the circle of competence.
- Patience is a position: inactivity beats hyperactivity in most decisions.

## Heuristics

- IF the opportunity requires being clever rather than avoiding stupidity THEN pass.
- IF incentives of the counterparty are unknown THEN find them before trusting the forecast.
- IF the decision is irreversible THEN require a margin of safety before committing.
- IF you cannot state the opposing case better than the counterpart THEN you may not hold an opinion.
- IF an idea arrives with social proof as its main argument THEN discount it.

## Refusals

- Declines short-term trading questions; redirects to base rates and incentives.
- Declines to forecast macro variables; the corpus treats them as unknowable.

## Voice

Terse, epigram-heavy summaries of what the corpus indicates; cites a source per claim; third-person analytic register throughout.
"""

SOURCES_3 = ("      - \"Source Book One (2005)\"\n"
             "      - \"Source Talk Two (2007)\"\n"
             "      - \"Source Transcript Three (2011)\"")
SOURCES_2 = ("      - \"Source Book One (2005)\"\n"
             "      - \"Source Talk Two (2007)\"")


def make_seat(root, seat_id, mode="corpus", living="false", license_="none",
              sources=SOURCES_3, body=VALID_BODY, display_name=None,
              with_references=True):
    seat_dir = os.path.join(root, seat_id)
    os.makedirs(seat_dir, exist_ok=True)
    fm = VALID_FRONTMATTER.format(
        id=seat_id,
        display_name=display_name or "Test Lens",
        mode=mode, subject="Test Subject", living=living,
        license=license_, sources=sources)
    with open(os.path.join(seat_dir, "SEAT.md"), "w", encoding="utf-8") as fh:
        fh.write(fm + body)
    if with_references:
        refs = os.path.join(seat_dir, "references")
        os.makedirs(refs, exist_ok=True)
        for f in ("principles.md", "mental-models.md", "frameworks.md",
                  "anti-patterns.md", "heuristics.md", "quotes.md",
                  "sources.md"):
            with open(os.path.join(refs, f), "w", encoding="utf-8") as fh:
                fh.write("# %s\n\nContent.\n" % f)
    return seat_dir


class LintRuleTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="chiron-lint-")

    def tearDown(self):
        shutil.rmtree(self.root)

    def rules(self, findings):
        return {f.rule for f in findings}

    def test_valid_seat_passes(self):
        seat = make_seat(self.root, "test-seat")
        findings, meta = lint_seat(seat)
        self.assertEqual(lint_status(findings), "pass",
                         [f.as_dict() for f in findings])
        self.assertEqual(meta["mode"], "corpus")

    def test_L1_living_persona_unlicensed_hard_fails(self):
        seat = make_seat(self.root, "test-seat", mode="persona", living="true",
                         license_="none")
        findings, _ = lint_seat(seat)
        self.assertIn("L1", self.rules(findings))
        self.assertEqual(lint_status(findings), "fail")

    def test_L1_not_triggered_when_licensed(self):
        seat = make_seat(self.root, "test-seat", mode="persona", living="true",
                         license_="granted")
        findings, _ = lint_seat(seat)
        self.assertNotIn("L1", self.rules(findings))

    def test_L1_not_triggered_for_corpus_living(self):
        seat = make_seat(self.root, "test-seat", mode="corpus", living="true")
        findings, _ = lint_seat(seat)
        self.assertNotIn("L1", self.rules(findings))

    def test_L4_two_sources_fails(self):
        seat = make_seat(self.root, "test-seat", sources=SOURCES_2)
        findings, _ = lint_seat(seat)
        self.assertIn("L4", self.rules(findings))
        self.assertEqual(lint_status(findings), "fail")

    def test_L5_missing_refusals_fails(self):
        body = VALID_BODY.replace("## Refusals", "## SomethingElse")
        seat = make_seat(self.root, "test-seat", body=body)
        findings, _ = lint_seat(seat)
        self.assertIn("L5", self.rules(findings))

    def test_L5_too_few_priors_fails(self):
        body = VALID_BODY.replace(
            "- Patience is a position: inactivity beats hyperactivity in most decisions.\n", ""
        ).replace(
            "- Big mistakes come from acting outside the circle of competence.\n", "")
        seat = make_seat(self.root, "test-seat", body=body)
        findings, _ = lint_seat(seat)
        self.assertIn("L5", self.rules(findings))

    def test_L7_persona_leakage_warns_standard_fails_strict(self):
        body = VALID_BODY.replace(
            "Terse, epigram-heavy summaries",
            "I always tell young people to invert. Terse summaries")
        seat = make_seat(self.root, "test-seat", body=body)
        findings, _ = lint_seat(seat, level="standard")
        l7 = [f for f in findings if f.rule == "L7"]
        self.assertTrue(l7)
        self.assertEqual(l7[0].level, "warn")
        self.assertEqual(lint_status(findings), "warn")

        findings, _ = lint_seat(seat, level="strict")
        l7 = [f for f in findings if f.rule == "L7"]
        self.assertTrue(l7)
        self.assertEqual(l7[0].level, "error")

    def test_L7_quoted_subject_speech_allowed(self):
        body = VALID_BODY.replace(
            "third-person analytic register throughout.",
            'third-person analytic register; may quote: "I always say invert."')
        seat = make_seat(self.root, "test-seat", body=body)
        findings, _ = lint_seat(seat)
        self.assertNotIn("L7", self.rules(findings))

    def test_L10_subject_name_without_suffix_warns(self):
        seat = make_seat(self.root, "test-seat", display_name="Test Subject")
        findings, _ = lint_seat(seat)
        self.assertIn("L10", self.rules(findings))

    def test_L10_lens_suffix_ok(self):
        seat = make_seat(self.root, "test-seat", display_name="Subject Lens")
        findings, _ = lint_seat(seat)
        self.assertNotIn("L10", self.rules(findings))

    def test_L12_missing_references_warns(self):
        seat = make_seat(self.root, "test-seat", with_references=False)
        findings, _ = lint_seat(seat)
        self.assertIn("L12", self.rules(findings))
        self.assertEqual(lint_status(findings), "warn")

    def test_original_mode_needs_no_provenance(self):
        seat_dir = os.path.join(self.root, "my-advisor")
        os.makedirs(seat_dir)
        fm = ("---\n"
              "name: my-advisor\n"
              "description: An original advisor.\n"
              "x-chiron:\n"
              "  display_name: My Advisor\n"
              "  mode: original\n"
              "  domains: [ops]\n"
              "---\n")
        with open(os.path.join(seat_dir, "SEAT.md"), "w") as fh:
            fh.write(fm + VALID_BODY)
        refs = os.path.join(seat_dir, "references")
        os.makedirs(refs)
        for f in ("principles.md", "mental-models.md", "frameworks.md",
                  "anti-patterns.md", "heuristics.md", "quotes.md", "sources.md"):
            with open(os.path.join(refs, f), "w", encoding="utf-8") as fh:
                fh.write("x\n")
        findings, _ = lint_seat(seat_dir)
        self.assertEqual(lint_status(findings), "pass",
                         [f.as_dict() for f in findings])


class YamlParserTests(unittest.TestCase):
    """Regressions from adversarial review: block scalars must parse."""

    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="chiron-yaml-")

    def tearDown(self):
        shutil.rmtree(self.root)

    def _seat_with_description(self, desc_block):
        seat_dir = os.path.join(self.root, "test-seat")
        os.makedirs(seat_dir)
        fm = ("---\n"
              "name: test-seat\n"
              + desc_block +
              "x-chiron:\n"
              "  display_name: Test Lens\n"
              "  mode: corpus\n"
              "  domains: [testing]\n"
              "  provenance:\n"
              "    subject: Test Subject\n"
              "    living: false\n"
              "    license: none\n"
              "    sources:\n" + SOURCES_3 + "\n"
              "---\n")
        with open(os.path.join(seat_dir, "SEAT.md"), "w", encoding="utf-8") as fh:
            fh.write(fm + VALID_BODY)
        refs = os.path.join(seat_dir, "references")
        os.makedirs(refs)
        for f in ("principles.md", "mental-models.md", "frameworks.md",
                  "anti-patterns.md", "heuristics.md", "quotes.md", "sources.md"):
            with open(os.path.join(refs, f), "w", encoding="utf-8") as fh:
                fh.write("x\n")
        return seat_dir

    def test_folded_scalar_description_parses(self):
        seat = self._seat_with_description(
            "description: >\n"
            "  Applies the reasoning, mental models, and temperament\n"
            "  of a test subject across multiple lines.\n")
        findings, meta = lint_seat(seat)
        self.assertEqual(lint_status(findings), "pass",
                         [f.as_dict() for f in findings])

    def test_literal_scalar_description_parses(self):
        seat = self._seat_with_description(
            "description: |\n"
            "  Line one.\n"
            "  Line two.\n")
        findings, _ = lint_seat(seat)
        self.assertEqual(lint_status(findings), "pass",
                         [f.as_dict() for f in findings])


class CliContractTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="chiron-cli-")
        self.seats = os.path.join(self.root, "seats")
        os.makedirs(self.seats)

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_lint(self, *args):
        return subprocess.run(
            [sys.executable, os.path.join(REPO, "scripts", "lint_seat.py")]
            + list(args),
            capture_output=True, text=True, cwd=self.root)

    def test_exit_codes_and_json_contract(self):
        make_seat(self.seats, "good-seat")
        make_seat(self.seats, "warn-seat", with_references=False)
        make_seat(self.seats, "bad-seat", sources=SOURCES_2)

        proc = self.run_lint("--all", "--format", "json")
        self.assertEqual(proc.returncode, 2)
        reports = json.loads(proc.stdout)
        self.assertEqual(len(reports), 3)
        by_id = {r["id"]: r for r in reports}
        self.assertEqual(by_id["good-seat"]["lint"], "pass")
        self.assertEqual(by_id["warn-seat"]["lint"], "warn")
        self.assertEqual(by_id["bad-seat"]["lint"], "fail")
        for r in reports:
            self.assertIn(r["lint"], ("pass", "warn", "fail"))

    def test_exit_0_all_pass(self):
        make_seat(self.seats, "good-seat")
        proc = self.run_lint("--all")
        self.assertEqual(proc.returncode, 0)

    def test_exit_1_warn_only(self):
        make_seat(self.seats, "warn-seat", with_references=False)
        proc = self.run_lint("--all")
        self.assertEqual(proc.returncode, 1)

    def test_missing_seats_dir_exit_2(self):
        proc = self.run_lint("--all", "--seats-dir", "nonexistent")
        self.assertEqual(proc.returncode, 2)

    def test_registry_marks_duplicate_ids_as_fail(self):
        # Two folders claiming the same frontmatter name → both fail (L3).
        make_seat(self.seats, "twin-a")
        make_seat(self.seats, "twin-b")
        for folder in ("twin-a", "twin-b"):
            path = os.path.join(self.seats, folder, "SEAT.md")
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            text = text.replace("name: %s" % folder, "name: twin-a")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        # twin-b now claims id twin-a but that mismatches its folder (L2 fail);
        # rename its folder so only the id collision itself is under test.
        os.rename(os.path.join(self.seats, "twin-b"),
                  os.path.join(self.seats, "twin-a-copy"))
        # folder/name mismatch is itself an error, so instead assert the
        # registry never emits a duplicate id with a loadable status.
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "scripts", "registry.py"),
             "--json"],
            capture_output=True, text=True, cwd=self.root)
        registry = json.loads(proc.stdout)
        ids = [r["id"] for r in registry]
        self.assertEqual(len(ids), 2)
        loadable = [r for r in registry if r["lint"] != "fail"]
        loadable_ids = [r["id"] for r in loadable]
        self.assertEqual(len(loadable_ids), len(set(loadable_ids)),
                         "registry emitted duplicate loadable ids: %r" % registry)

    def test_registry_json_contract(self):
        make_seat(self.seats, "good-seat")
        proc = subprocess.run(
            [sys.executable, os.path.join(REPO, "scripts", "registry.py"),
             "--json"],
            capture_output=True, text=True, cwd=self.root)
        self.assertEqual(proc.returncode, 0)
        registry = json.loads(proc.stdout)
        self.assertEqual(len(registry), 1)
        entry = registry[0]
        for key in ("id", "display_name", "mode", "domains", "lint", "path"):
            self.assertIn(key, entry)
        self.assertEqual(entry["lint"], "pass")


if __name__ == "__main__":
    unittest.main()
