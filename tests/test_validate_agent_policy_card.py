from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

import validate_agent_policy_card as validator


REPO_ROOT = Path(__file__).resolve().parents[1]
UNSAFE_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "unsafe_authority_policy_card.md"


class ValidateAgentPolicyCardTests(unittest.TestCase):
    def test_unsafe_authority_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(UNSAFE_FIXTURE)

        self.assertFalse(ok)
        self.assertIn("path mention is too broad/unsafe: /", failures)
        self.assertIn("missing explicit no-runtime-grant boundary", failures)

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


if __name__ == "__main__":
    unittest.main()
