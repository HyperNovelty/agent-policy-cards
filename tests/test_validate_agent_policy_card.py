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
