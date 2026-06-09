#!/usr/bin/env python3
"""Stdlib validator for local Verifiable Research Packets.

Usage:
  python3 scripts/validate_verifiable_research_packet.py path/to/research_packets/packet_dir
"""
import json
import sys
from pathlib import Path

ALLOWED_APPROVAL = {
    "draft_packet", "ready_for_human_review", "needs_more_sources",
    "approved_for_internal_use", "approved_for_draft_use", "approved_for_public_use",
    "blocked", "archived",
}
ALLOWED_CLAIM_TYPES = {"factual", "interpretive", "strategic", "product_implication", "risk_warning"}
ALLOWED_VERIFY = {"verified_strongly", "verified_lightly", "not_verified", "contradicted", "source_limited"}
ALLOWED_PUBLIC = {"usable", "usable_with_caveat", "internal_only", "blocked"}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return f"JSON_ERROR: {exc}"


def require_keys(obj, keys, label, errors):
    for key in keys:
        if key not in obj or obj[key] in (None, "", []):
            errors.append(f"{label}: missing/empty {key}")


def packet_status(packet_md):
    for line in packet_md.splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip().strip("`")
    return ""


def validate(packet_dir):
    p = Path(packet_dir)
    errors = []
    warnings = []
    required_files = ["PACKET.md", "source_ledger.json", "claim_ledger.json", "verifier_checklist.md", "dashboard_review_card.md"]
    for name in required_files:
        if not (p / name).exists():
            errors.append(f"missing required file: {name}")

    packet_text = (p / "PACKET.md").read_text(encoding="utf-8") if (p / "PACKET.md").exists() else ""
    status = packet_status(packet_text)
    if status and status not in ALLOWED_APPROVAL:
        errors.append(f"PACKET.md status not controlled value: {status}")
    if "Public side effects: none" not in packet_text:
        errors.append("PACKET.md must include 'Public side effects: none'")

    sources = load_json(p / "source_ledger.json") if (p / "source_ledger.json").exists() else []
    claims = load_json(p / "claim_ledger.json") if (p / "claim_ledger.json").exists() else []
    visuals_path = p / "visual_evidence.json"
    visuals = load_json(visuals_path) if visuals_path.exists() else []

    if isinstance(sources, str):
        errors.append(sources)
        sources = []
    if isinstance(claims, str):
        errors.append(claims)
        claims = []
    if isinstance(visuals, str):
        errors.append(visuals)
        visuals = []

    source_ids = set()
    for i, src in enumerate(sources):
        label = f"source[{i}]"
        require_keys(src, ["source_id", "url", "title", "source_type", "source_state", "local_evidence_path", "public_quote_allowed", "notes"], label, errors)
        sid = src.get("source_id")
        if sid in source_ids:
            errors.append(f"duplicate source_id: {sid}")
        source_ids.add(sid)
        ev = src.get("local_evidence_path")
        if ev and not (p / ev).exists():
            warnings.append(f"{label}: local evidence path not found: {ev}")
        if src.get("public_quote_allowed") is True and src.get("source_state") not in {"full_text_captured"}:
            warnings.append(f"{label}: public_quote_allowed true while source_state is not full_text_captured")

    claim_ids = set()
    for i, clm in enumerate(claims):
        label = f"claim[{i}]"
        require_keys(clm, ["claim_id", "claim_text", "claim_type", "source_ids", "evidence_quote_or_pointer", "verification_status", "public_use_status", "risk_tags", "reviewer_note"], label, errors)
        cid = clm.get("claim_id")
        if cid in claim_ids:
            errors.append(f"duplicate claim_id: {cid}")
        claim_ids.add(cid)
        if clm.get("claim_type") not in ALLOWED_CLAIM_TYPES:
            errors.append(f"{label}: invalid claim_type {clm.get('claim_type')}")
        if clm.get("verification_status") not in ALLOWED_VERIFY:
            errors.append(f"{label}: invalid verification_status {clm.get('verification_status')}")
        if clm.get("public_use_status") not in ALLOWED_PUBLIC:
            errors.append(f"{label}: invalid public_use_status {clm.get('public_use_status')}")
        for sid in clm.get("source_ids", []):
            if sid not in source_ids:
                errors.append(f"{label}: unknown source_id {sid}")
        if clm.get("public_use_status") == "usable" and clm.get("verification_status") not in {"verified_strongly", "verified_lightly"}:
            warnings.append(f"{label}: usable claim is not verified strongly/lightly")

    for i, vis in enumerate(visuals):
        label = f"visual[{i}]"
        require_keys(vis, ["visual_id", "source_id", "file_path", "captured_date", "what_it_shows", "used_for_claim_ids", "limitations"], label, errors)
        if vis.get("source_id") and vis.get("source_id") not in source_ids:
            errors.append(f"{label}: unknown source_id {vis.get('source_id')}")
        for cid in vis.get("used_for_claim_ids", []):
            if cid not in claim_ids:
                errors.append(f"{label}: unknown claim_id {cid}")

    return errors, warnings


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    errors, warnings = validate(argv[1])
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: packet valid ({len(warnings)} warning(s))")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
