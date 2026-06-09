#!/usr/bin/env python3
"""Static validator for Agent Policy Cards.

Local-only / advisory. This script reads Markdown policy cards and checks for
required sections, explicit blocked-action language, evidence/audit fields, and
high-level governance categories. It does not execute card contents and does not
grant runtime authority.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

PROJECT_ROOT = Path(__file__).resolve().parent

REQUIRED_HEADINGS = [
    "job identity",
    "allowed scope",
    "explicit exclusions",
    "evidence required before reporting success",
    "public/account/paid-action gates",
    "budgets and limits",
    "stop conditions",
    "human review point",
    "audit-log fields",
    "governance category map",
]

REQUIRED_BLOCKED_TERMS = [
    "credential",
    "public",
    "account",
    "paid",
    "deploy",
    "publish",
]

REQUIRED_AUDIT_FIELDS = [
    "run_id",
    "policy_card_path",
    "files",
    "verification",
    "blocked_actions",
    "next_safe_action",
]

REQUIRED_CATEGORIES = [
    "policy",
    "identity",
    "sandbox",
    "audit",
    "kill switch",
    "budget",
    "provenance",
    "compliance evidence",
]

PLACEHOLDER_MARKERS = ["<short stable name>", "<what useful outcome", "<exact local", "<approved source", "<exact destination", "<search/read", "<e.g."]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def heading_texts(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,4}\s+(.*)$", line.strip())
        if match:
            title = re.sub(r"^\d+\.\s*", "", match.group(1).strip().lower())
            out.append(title)
    return out


def path_mentions(text: str) -> list[str]:
    mentions: list[str] = []
    # Markdown/code-ish local paths only; URLs are intentionally ignored.
    for raw in re.findall(r"`([^`]+)`", text):
        if "/" in raw or raw.startswith("C:\\"):
            mentions.append(raw)
    return mentions


def is_broad_root(raw: str) -> bool:
    clean = raw.strip()
    broad = {"/", "~", "/home", "/home/aware1", "/home/aware1/.hermes", "/mnt/c", "C:\\", "C:\\Users", "C:\\Users\\Aware1"}
    if clean in broad:
        return True
    if ".." in Path(clean.replace("C:\\", "/mnt/c/")).parts:
        return True
    return False


def validate_text(text: str, *, allow_template_placeholders: bool = False) -> list[str]:
    failures: list[str] = []
    norm = normalize(text)
    headings = heading_texts(text)

    for required in REQUIRED_HEADINGS:
        if not any(required in h for h in headings):
            failures.append(f"missing required heading: {required}")

    for term in REQUIRED_BLOCKED_TERMS:
        if term not in norm:
            failures.append(f"missing blocked-action/gate term: {term}")

    for field in REQUIRED_AUDIT_FIELDS:
        if field not in norm:
            failures.append(f"missing audit/evidence field marker: {field}")

    for category in REQUIRED_CATEGORIES:
        if category not in norm:
            failures.append(f"missing governance category: {category}")

    if "runtime permission grant" not in norm and "not a runtime" not in norm:
        failures.append("missing explicit no-runtime-grant boundary")

    if "human approval" not in norm and "human review" not in norm and "jordan" not in norm:
        failures.append("missing human approval/review language")

    if not allow_template_placeholders:
        for marker in PLACEHOLDER_MARKERS:
            if marker.lower() in text.lower():
                failures.append(f"unfilled template placeholder remains: {marker}")

    for mention in path_mentions(text):
        if is_broad_root(mention):
            failures.append(f"path mention is too broad/unsafe: {mention}")

    return failures


def validate_file(path: Path, *, allow_template_placeholders: bool = False) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    failures = validate_text(text, allow_template_placeholders=allow_template_placeholders)
    return not failures, failures


def run_self_test() -> int:
    good = """# Agent Policy Card — Toy

**Boundary:** local/static only; not a runtime permission grant.

## 1. Job identity
- **Job / worker name:** toy
- **Purpose:** local test

## 2. Allowed scope
- `products/agent_os_authority_layer/examples/toy.md`

## 3. Explicit exclusions
- credentials, account sessions, public deploy, publish, paid actions

## 4. Evidence required before reporting success
- files exist
- verification passes

## 5. Public/account/paid-action gates
Blocked without explicit human approval.

## 6. Budgets and limits
- one pass

## 7. Stop conditions
Stop on credential/account/public/paid/deploy/publish need.

## 8. Human review point
Jordan review.

## 9. Audit-log fields
`run_id`, `policy_card_path`, `files`, `verification`, `blocked_actions`, `next_safe_action`

## 10. Governance category map
Policy, identity, sandbox, audit, kill switch, budget, provenance, compliance evidence.
"""
    bad = "# Agent Policy Card — Bad\n\nDo stuff.\n"
    with TemporaryDirectory() as tmp:
        good_path = Path(tmp) / "good.md"
        bad_path = Path(tmp) / "bad.md"
        good_path.write_text(good, encoding="utf-8")
        bad_path.write_text(bad, encoding="utf-8")
        good_ok, good_failures = validate_file(good_path)
        bad_ok, bad_failures = validate_file(bad_path)
    if not good_ok:
        print("SELF_TEST_FAIL: good fixture failed")
        for failure in good_failures:
            print(" -", failure)
        return 1
    if bad_ok:
        print("SELF_TEST_FAIL: bad fixture passed unexpectedly")
        return 1
    print("SELF_TEST_PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate static Agent Policy Card Markdown files.")
    parser.add_argument("paths", nargs="*", help="Markdown card paths to validate")
    parser.add_argument("--self-test", action="store_true", help="run built-in validator self-test")
    parser.add_argument("--allow-template-placeholders", action="store_true", help="allow template placeholder markers")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.paths:
        parser.error("provide at least one path or --self-test")

    any_failed = False
    for raw in args.paths:
        path = Path(raw)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if not path.exists():
            print(f"FAIL {raw}: file not found")
            any_failed = True
            continue
        ok, failures = validate_file(path, allow_template_placeholders=args.allow_template_placeholders)
        rel = path if not str(path).startswith(str(PROJECT_ROOT)) else path.relative_to(PROJECT_ROOT)
        if ok:
            print(f"PASS {rel}")
        else:
            print(f"FAIL {rel}")
            for failure in failures:
                print(f"  - {failure}")
            any_failed = True
    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
