#!/usr/bin/env python3
"""Report-only registry checker for Agent Policy Cards.

This checker maps known worker lanes to expected static policy cards and reports
whether each card exists, is stale, or fails the advisory Markdown validator. It
is intentionally non-enforcing: missing/stale/invalid cards are printed as local
QA findings, not used to block jobs, alter cron, grant permissions, or authorize
runtime behavior.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_REGISTRY = PROJECT_ROOT / "policy_card_registry.json"
VALIDATOR = PROJECT_ROOT / "validate_agent_policy_card.py"


def parse_date(raw: str | None) -> date | None:
    if not raw:
        return None
    return datetime.strptime(raw, "%Y-%m-%d").date()


def load_registry(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("registry root must be an object")
    if data.get("mode") != "report_only_no_runtime_enforcement":
        raise ValueError("registry mode must be report_only_no_runtime_enforcement")
    lanes = data.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        raise ValueError("registry must contain a non-empty lanes list")
    return data


def run_card_validator(rel_path: str) -> tuple[bool, str]:
    cmd = [sys.executable, str(VALIDATOR), rel_path]
    proc = subprocess.run(cmd, cwd=PROJECT_ROOT, text=True, capture_output=True)
    output = (proc.stdout + proc.stderr).strip()
    return proc.returncode == 0, output


def check_registry(registry: dict[str, Any], *, today: date) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    summary = {"ok": 0, "missing": 0, "stale": 0, "validator_failure": 0}

    for lane in registry["lanes"]:
        lane_id = lane.get("lane_id") or "<missing-lane-id>"
        rel = lane.get("policy_card_path")
        next_due = parse_date(lane.get("next_review_due"))
        statuses: list[str] = []
        validator_output = ""
        card_exists = False

        if not rel:
            statuses.append("missing")
            summary["missing"] += 1
        else:
            path = PROJECT_ROOT / rel
            card_exists = path.exists() and path.is_file()
            if not card_exists:
                statuses.append("missing")
                summary["missing"] += 1
            else:
                ok, validator_output = run_card_validator(rel)
                if ok:
                    statuses.append("ok")
                else:
                    statuses.append("validator_failure")
                    summary["validator_failure"] += 1

        if next_due and next_due < today:
            statuses.append("stale")
            summary["stale"] += 1

        if statuses == ["ok"]:
            summary["ok"] += 1

        findings.append(
            {
                "lane_id": lane_id,
                "lane_label": lane.get("lane_label"),
                "policy_card_path": rel,
                "card_exists": card_exists,
                "next_review_due": lane.get("next_review_due"),
                "statuses": statuses,
                "report_only": True,
                "validator_output": validator_output,
                "blocked_expansion_without_new_card": lane.get("blocked_expansion_without_new_card", []),
            }
        )

    return {
        "checked_at": today.isoformat(),
        "mode": registry.get("mode"),
        "boundary": registry.get("boundary"),
        "summary": summary,
        "findings": findings,
        "enforcement": "none_report_only",
    }


def print_markdown(report: dict[str, Any]) -> None:
    print("# Agent Policy Card Registry Check — Report Only")
    print()
    print(f"Checked: {report['checked_at']}")
    print(f"Mode: `{report['mode']}`")
    print("Enforcement: none — report only")
    print()
    print(report["boundary"])
    print()
    s = report["summary"]
    print("## Summary")
    print(f"- OK: {s['ok']}")
    print(f"- Missing: {s['missing']}")
    print(f"- Stale: {s['stale']}")
    print(f"- Validator failure: {s['validator_failure']}")
    print()
    print("## Findings")
    for item in report["findings"]:
        print(f"- **{item['lane_id']}** — {', '.join(item['statuses'])}")
        print(f"  - Card: `{item['policy_card_path']}`")
        print(f"  - Next review due: `{item['next_review_due']}`")
        if item["validator_output"]:
            compact = item["validator_output"].replace("\n", " | ")
            print(f"  - Validator: `{compact}`")
    print()
    print("> Boundary: findings are advisory. Do not use this report to grant runtime permission, alter cron, install toolkits, wire MCP, or take public/account/paid/destructive actions.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Agent Policy Card registry in report-only mode.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="registry JSON path")
    parser.add_argument("--today", default=date.today().isoformat(), help="YYYY-MM-DD override for deterministic checks")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    args = parser.parse_args(argv)

    registry_path = Path(args.registry)
    if not registry_path.is_absolute():
        registry_path = PROJECT_ROOT / registry_path
    registry = load_registry(registry_path)
    report = check_registry(registry, today=parse_date(args.today) or date.today())
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_markdown(report)
    # This is a report-only checker. Missing/stale/invalid cards do not produce a
    # non-zero exit code. Malformed registry/JSON still raises before this point.
    return 0


if __name__ == "__main__":
    sys.exit(main())
