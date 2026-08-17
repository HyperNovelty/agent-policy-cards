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
ISSUE_TRIAGE_UNSAFE_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "issue_triage_mutation_promotion_policy_card.md"
BOUNDED_ISSUE_TRIAGE_CARD = REPO_ROOT / "examples" / "AGENT_POLICY_CARD_BOUNDED_ISSUE_TRIAGE_LANE_2026-08-17.md"


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
            "The code-review agent may modify files after inspection.",
            "For code review, the agent is permitted to edit files.",
            "During review,\n the agent can patch defects in place.",
            "During review, the agent is allowed to write fixes.",
            "The code reviewer may edit files after inspection.",
            "The code review lane is allowed to format files.",
            "The code review worker is authorized to commit fixes.",
            "The agent may branch during review when fixes are obvious.",
            "The agent can submit review changes during review.",
            "During review the agent may merge branches.",
            "During review the agent can push fixes.",
            "During code review, the agent may apply fixes.",
            "During code review, the agent may not only inspect files but also edit them.",
            "The code reviewer may not only inspect but also modify files.",
            "During code review, the agent may not just inspect; it may also patch defects.",
            "Editing files is allowed during code review.",
            "During code review, edits are permitted.",
            "The code-review agent has permission to edit files.",
            "The code-review agent may update files.",
            "The code-review agent may rewrite files.",
            "The code-review agent may delete files.",
            "The code-review agent may create files.",
            "Code reviewers may edit files.",
            "Code review agents are allowed to edit files.",
            "The code review agents are authorized to delete files.",
            "During code review, edits by the review agent are permitted.",
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
            "The code-review agent may never edit files.",
            "During review the agent cannot patch defects.",
            "During code review, the agent may inspect files but cannot edit them.",
            "For code review, the agent is not permitted to commit fixes.",
            "The code review agent may only inspect, not patch files.",
            "During code review, the agent may write findings for the human reviewer.",
            "During code review, the agent may write a report but may not write files.",
            "During code review, the agent may suggest fixes but cannot apply them.",
            "The code-review agent may inspect files, and the implementation agent may edit them.",
            "- The review agent may inspect files.\n- A separate implementation agent may edit files.",
            "During code review, edits by the implementation agent are permitted.",
            "During code review, edits are permitted for the implementation agent, not the review agent.",
            "During code review, edits are permitted for the implementation agents.",
            "During code review, edits by implementation agents are permitted.",
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

    def test_issue_triage_mutation_promotion_fixture_fails_with_expected_findings(self) -> None:
        ok, failures = validator.validate_file(ISSUE_TRIAGE_UNSAFE_FIXTURE)

        self.assertFalse(ok)
        self.assertTrue(
            any("unsafe issue-triage mutation authority detected" in failure for failure in failures),
            failures,
        )
        self.assertTrue(
            any("unsafe issue-triage recommendation promotion detected" in failure for failure in failures),
            failures,
        )

    def test_issue_triage_authority_affirmative_variants_fail(self) -> None:
        cases = [
            "The issue-triage agent may comment on the GitHub issue after review.",
            "Issue-triage agents may patch repository issues after review.",
            "For issue triage, the agent is permitted to label defects as bug.",
            "The triage lane is authorized to assign repository issues to maintainers.",
            "The triage workers are allowed to close duplicate issues.",
            "During issue triage, state changes are allowed.",
            "During issue triage, labels are allowed.",
            "The issue-triage recommendation is a maintainer decision.",
            "The triage recommendation is not a decision; it is an assignment.",
            "The triage recommendation is not accepted; it becomes a priority.",
            "The triage report decides the issue priority.",
        ]

        for text in cases:
            with self.subTest(text=text):
                failures = validator.validate_text(text, allow_template_placeholders=True)

                self.assertTrue(
                    any("unsafe issue-triage" in failure for failure in failures),
                    failures,
                )

    def test_issue_triage_authority_denials_do_not_false_positive(self) -> None:
        cases = [
            "The issue-triage agent may not comment on issues.",
            "For issue triage, the agent is not permitted to label defects.",
            "The triage lane may draft a recommendation but must not assign issues.",
            "Issue triage recommendations are not maintainer decisions.",
            "The issue packet may include labels already present as source facts.",
            "During issue triage, labels already present in the supplied packet are allowed as source facts.",
            "During issue triage, assignments already recorded on the supplied repository issue are permitted as source evidence.",
            "During issue triage, milestones from the issue packet are authorized as evidence.",
            "Human approval is required before later GitHub comments, labels, assignments, or closure.",
            "During issue triage, a separate implementation agent may patch the bug after explicit human approval.",
            "During issue triage, separate implementation agents may patch bugs after explicit human approval.",
            "The issue-triage agent may draft a recommendation; after approval, a human maintainer may comment on the issue.",
            "The issue-triage agents may draft recommendations; after approval, human maintainers may label issues.",
            "During issue triage, comments by human maintainers are permitted after explicit approval.",
        ]

        for text in cases:
            with self.subTest(text=text):
                failures = validator.validate_text(text, allow_template_placeholders=True)

                self.assertFalse(
                    any("unsafe issue-triage" in failure for failure in failures),
                    failures,
                )

    def test_bounded_issue_triage_card_passes(self) -> None:
        ok, failures = validator.validate_file(BOUNDED_ISSUE_TRIAGE_CARD)

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
