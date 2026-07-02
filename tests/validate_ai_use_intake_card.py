#!/usr/bin/env python3
"""Validate local AI Use Intake Card fixtures.

This is a stdlib-only deterministic validator for public-safe intake examples.
It checks shape and safety boundaries; it does not grant deployment,
compliance, enforcement, legal, public-action, account-action, or runtime
authority.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "ai_use_intake_card.schema.json"
VALID_FIXTURES = [ROOT / "examples" / "ai_use_intake_card.customer_support_fixture.json"]
INVALID_FIXTURES = [ROOT / "examples" / "invalid" / "ai_use_intake_card.automated_action_no_review.json"]

REQUIRED_KEYS = [
    "card_type",
    "status",
    "system_name",
    "owner",
    "business_purpose",
    "build_or_buy",
    "vendor_or_model",
    "data_touched",
    "sensitive_data_possible",
    "decision_or_output",
    "affected_people",
    "consequential_decision_exposure",
    "human_review_required",
    "non_ai_alternative",
    "initial_route",
    "missing_evidence",
    "synthetic_evidence_attached",
    "next_gate",
    "not_approval_statement",
]

ENUMS = {
    "status": {"sample_local_only", "draft_local_only"},
    "build_or_buy": {"build_custom", "buy_or_configure_existing_model", "undecided"},
    "consequential_decision_exposure": {
        "none",
        "limited_with_human_review",
        "possible_if_automated",
        "high_if_automated",
    },
    "initial_route": {
        "document_only",
        "assess",
        "requires_policy_card",
        "requires_authority_envelope",
        "do_not_proceed",
    },
    "next_gate": {"policy_card", "authority_envelope", "evidence_review", "human_review", "do_not_proceed"},
}

STRING_ARRAY_KEYS = {
    "data_touched",
    "affected_people",
    "missing_evidence",
    "synthetic_evidence_attached",
}

PRIVATE_OR_SECRET_PATTERNS = [
    r"/home/",
    r"file:///home/",
    r"C:\\Users\\",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
    r"\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}",
]

AUTONOMOUS_ACTION_PATTERNS = [
    r"\b(send|sends|sent)\b.{0,80}\b(email|emails|message|messages|reply|replies)\b",
    r"\b(post|posts|posted|publish|publishes|published)\b.{0,80}\b(public|publicly|social|web)\b",
    r"\b(change|changes|changed|edit|edits|edited)\b.{0,80}\b(account settings|account)\b",
    r"\b(approve|approves|approved|decide|decides|determines?)\b.{0,80}\b(refund|refunds|eligibility|benefit|access)\b",
    r"\b(takes?|execute|executes|performs?)\b.{0,80}\b(consequential action|account action|public action)\b",
]

APPROVAL_CLAIM_PATTERNS = [
    r"\b(compliance|legal|deployment|production|operate|operation)\b.{0,80}\b(approval|approved|certification|certifies|certified)\b",
    r"\bapproval to deploy\b",
    r"\bpermission to operate\b",
]

STRICT_NEXT_GATES = {"policy_card", "authority_envelope", "human_review", "do_not_proceed"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def all_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for item in value:
            out.extend(all_strings(item))
        return out
    if isinstance(value, dict):
        out = []
        for item in value.values():
            out.extend(all_strings(item))
        return out
    return []


def has_review_language(doc: dict[str, Any]) -> bool:
    text = " ".join(all_strings(doc)).lower()
    return bool(doc.get("human_review_required")) and ("human review" in text or "reviewer" in text)


def validate_doc(doc: Any) -> list[str]:
    failures: list[str] = []
    if not isinstance(doc, dict):
        return ["root must be an object"]

    extra = sorted(set(doc) - set(REQUIRED_KEYS))
    missing = [key for key in REQUIRED_KEYS if key not in doc]
    if extra:
        failures.append(f"unexpected keys: {', '.join(extra)}")
    for key in missing:
        failures.append(f"missing key: {key}")
    if missing:
        return failures

    if doc.get("card_type") != "ai_use_intake":
        failures.append("card_type must be ai_use_intake")
    for key, allowed in ENUMS.items():
        if doc.get(key) not in allowed:
            failures.append(f"{key} invalid: {doc.get(key)!r}")
    if not isinstance(doc.get("sensitive_data_possible"), bool):
        failures.append("sensitive_data_possible must be boolean")
    if not isinstance(doc.get("human_review_required"), bool):
        failures.append("human_review_required must be boolean")

    for key in REQUIRED_KEYS:
        if key in STRING_ARRAY_KEYS:
            value = doc.get(key)
            if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
                failures.append(f"{key} must be an array of non-empty strings")
        elif key not in {"sensitive_data_possible", "human_review_required"} and not isinstance(doc.get(key), str):
            failures.append(f"{key} must be a string")

    if not doc.get("data_touched"):
        failures.append("data_touched must be non-empty")
    if not doc.get("affected_people"):
        failures.append("affected_people must be non-empty")
    if not doc.get("missing_evidence"):
        failures.append("missing_evidence must be non-empty")

    text = "\n".join(all_strings(doc))
    for pattern in PRIVATE_OR_SECRET_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"private path or secret-like material detected: {pattern}")

    action_claimed = any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in AUTONOMOUS_ACTION_PATTERNS)
    consequential = doc.get("consequential_decision_exposure") in {"possible_if_automated", "high_if_automated"}
    if (action_claimed or consequential) and not has_review_language(doc):
        failures.append("consequential or action-taking use requires explicit human review")
    if action_claimed and doc.get("next_gate") not in STRICT_NEXT_GATES:
        failures.append("action-taking use requires a stricter next_gate")
    if consequential and doc.get("next_gate") not in STRICT_NEXT_GATES:
        failures.append("consequential exposure requires a stricter next_gate")

    approval_text = "\n".join(str(doc.get(key, "")) for key in ["business_purpose", "decision_or_output"])
    for pattern in APPROVAL_CLAIM_PATTERNS:
        if re.search(pattern, approval_text, flags=re.IGNORECASE):
            failures.append(f"approval/compliance/deployment claim detected: {pattern}")

    boundary = str(doc.get("not_approval_statement", "")).lower()
    for phrase in ["not compliance approval", "deployment approval", "legal advice", "permission to operate"]:
        if phrase not in boundary:
            failures.append(f"not_approval_statement missing boundary phrase: {phrase}")

    return failures


def validate_file(path: Path) -> tuple[bool, list[str]]:
    try:
        doc = load(path)
    except json.JSONDecodeError as exc:
        return False, [f"invalid JSON: {exc}"]
    failures = validate_doc(doc)
    return not failures, failures


def main() -> int:
    schema = load(SCHEMA)
    if schema.get("properties", {}).get("card_type", {}).get("const") != "ai_use_intake":
        print("ai_use_intake_validation=failed error=schema card_type const missing", file=sys.stderr)
        return 1

    failed = False
    valid_count = 0
    invalid_count = 0
    for path in VALID_FIXTURES:
        ok, failures = validate_file(path)
        rel = path.relative_to(ROOT)
        if ok:
            valid_count += 1
            print(f"PASS valid {rel}")
        else:
            failed = True
            print(f"FAIL valid {rel}", file=sys.stderr)
            for failure in failures:
                print(f"  - {failure}", file=sys.stderr)

    for path in INVALID_FIXTURES:
        ok, failures = validate_file(path)
        rel = path.relative_to(ROOT)
        if ok:
            failed = True
            print(f"FAIL invalid {rel} passed unexpectedly", file=sys.stderr)
        else:
            invalid_count += 1
            print(f"PASS invalid {rel} blocked_findings={len(failures)}")

    if failed:
        print("ai_use_intake_validation=failed", file=sys.stderr)
        return 1
    print(f"validated_ai_use_intake_cards={valid_count}")
    print(f"blocked_invalid_ai_use_intake_cards={invalid_count}")
    print("ai_use_intake_validation=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
