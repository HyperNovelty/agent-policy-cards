from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

import validate_agent_policy_card as validator


UNSAFE_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "unsafe_authority_policy_card.md"
SECRET_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "secret_like_policy_card.md"
SECRET_SEARCH_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "secret_search_policy_card.md"
UNGATED_PUBLIC_ACCOUNT_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "ungated_public_account_policy_card.md"
CODE_REVIEW_MUTATING_AUTHORITY_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "code_review_mutating_authority_policy_card.md"
READ_ONLY_CODE_REVIEW_CARD = REPO_ROOT / "examples" / "AGENT_POLICY_CARD_READ_ONLY_CODE_REVIEW_LANE_2026-07-31.md"


class ValidateAgentPolicyCardTests(unittest.TestCase):
    def test_unsafe_authority_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(UNSAFE_FIXTURE)

        self.assertFalse(ok)
        self.assertIn("path mention is too broad/unsafe: /", failures)
        self.assertIn("missing explicit no-runtime-grant boundary", failures)
        self.assertIn(
            "unsafe authority expansion language detected: grant itself runtime permission",
            failures,
        )

    def test_secret_like_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(SECRET_FIXTURE)

        self.assertFalse(ok)
        self.assertIn("secret-like material detected: -----BEGIN [A-Z ]*PRIVATE KEY-----", failures)
        self.assertIn(r"secret-like material detected: \bghp_[A-Za-z0-9]{20,}\b", failures)

    def test_secret_search_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(SECRET_SEARCH_FIXTURE)

        self.assertFalse(ok)
        self.assertIn(
            r"unsafe secret-search authority detected: \b(search|scan|grep|find|look for)\b.{0,80}\b(api keys?|secrets?|tokens?|credentials?)\b",
            failures,
        )

    def test_ungated_public_account_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(UNGATED_PUBLIC_ACCOUNT_FIXTURE)

        self.assertFalse(ok)
        self.assertIn(
            r"ungated public/account authority detected: \b(publish|post|upload|share|change account settings|edit account settings)\b.{0,120}\b(without|no)\b.{0,40}\b(explicit )?(human )?(approval|review)\b",
            failures,
        )

    def test_code_review_mutating_authority_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(CODE_REVIEW_MUTATING_AUTHORITY_FIXTURE)

        self.assertFalse(ok)
        self.assertTrue(
            any("unsafe code-review mutation authority detected" in failure for failure in failures),
            failures,
        )
        self.assertIn(
            r"unsafe secret-search authority detected: \b(search|scan|grep|find|look for)\b.{0,80}\b(api keys?|secrets?|tokens?|credentials?)\b",
            failures,
        )

    def test_code_review_mutating_authority_affirmative_variants_fail(self) -> None:
        cases = [
            "The code-review agent may edit files after inspection.",
            "For code review, the agent is permitted to edit files.",
            "During review,\n the agent can patch defects in place.",
            "The code review lane is allowed to format files.",
            "The code review worker is authorized to commit fixes.",
            "The agent may branch during review when fixes are obvious.",
            "The agent can submit review changes during review.",
            "During review the agent may merge branches.",
            "During review the agent can push fixes.",
        ]

        for text in cases:
            with self.subTest(text=text):
                failures = validator.validate_text(text, allow_template_placeholders=True)

                self.assertTrue(
                    any("unsafe code-review mutation authority detected" in failure for failure in failures),
                    failures,
                )

    def test_code_review_mutating_authority_denials_do_not_false_positive(self) -> None:
        cases = [
            "The code-review agent may not edit files.",
            "During review the agent cannot patch defects.",
            "For code review, the agent is not permitted to commit fixes.",
        ]

        for text in cases:
            with self.subTest(text=text):
                failures = validator.validate_text(text, allow_template_placeholders=True)

                self.assertFalse(
                    any("unsafe code-review mutation authority detected" in failure for failure in failures),
                    failures,
                )

    def test_read_only_code_review_card_passes(self) -> None:
        ok, failures = validator.validate_file(READ_ONLY_CODE_REVIEW_CARD)

        self.assertTrue(ok, failures)

    def test_cli_validates_repo_local_example_path(self) -> None:
        cmd = [
            sys.executable,
            str(REPO_ROOT / "validate_agent_policy_card.py"),
            "examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md",
        ]
        proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(
            "PASS examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md",
            proc.stdout,
        )

    def test_cli_json_report_is_machine_readable_and_deterministic(self) -> None:
        cmd = [
            sys.executable,
            str(REPO_ROOT / "validate_agent_policy_card.py"),
            "--json",
            "examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md",
            "tests/fixtures/secret_like_policy_card.md",
        ]
        proc = subprocess.run(cmd, cwd=REPO_ROOT, text=True, capture_output=True, check=False)

        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        report = json.loads(proc.stdout)
        self.assertEqual(report["report_version"], 1)
        self.assertEqual(report["summary"], {"failed": 1, "missing": 0, "passed": 1, "total": 2})
        self.assertEqual(
            [item["path"] for item in report["results"]],
            [
                "examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md",
                "tests/fixtures/secret_like_policy_card.md",
            ],
        )
        self.assertTrue(report["results"][0]["ok"])
        self.assertFalse(report["results"][1]["ok"])


if __name__ == "__main__":
    unittest.main()
