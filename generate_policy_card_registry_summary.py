#!/usr/bin/env python3
"""Generate dashboard-facing Agent Policy Card registry summary.

Report-only local visibility. This script consumes check_policy_card_registry.py
output and writes compact JSON/Markdown summaries for the Command Center. It does
not enforce, block, schedule, grant authority, modify Hermes config, or run jobs.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent
CHECKER = PROJECT_ROOT / "check_policy_card_registry.py"
OUT_JSON = PROJECT_ROOT / "dashboard/policy_card_registry_summary.json"
OUT_MD = PROJECT_ROOT / "dashboard/POLICY_CARD_REGISTRY_SUMMARY.md"


def run_checker(today: str) -> dict[str, Any]:
    proc = subprocess.run(
        [sys.executable, str(CHECKER), "--today", today, "--json"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(proc.stdout)


def compact_summary(report: dict[str, Any]) -> dict[str, Any]:
    summary = report["summary"]
    attention = []
    for item in report["findings"]:
        statuses = set(item.get("statuses", []))
        if statuses - {"ok"}:
            attention.append(
                {
                    "lane_id": item["lane_id"],
                    "lane_label": item.get("lane_label"),
                    "statuses": item.get("statuses", []),
                    "policy_card_path": item.get("policy_card_path"),
                    "next_review_due": item.get("next_review_due"),
                    "report_only": True,
                }
            )
    return {
        "generated_at": report["checked_at"],
        "title": "Agent Policy Card Registry Summary",
        "mode": report["mode"],
        "enforcement": report["enforcement"],
        "report_only": True,
        "counts": {
            "ok_cards": summary["ok"],
            "missing_cards": summary["missing"],
            "stale_cards": summary["stale"],
            "validator_failures": summary["validator_failure"],
        },
        "attention_lanes": attention,
        "boundary": "Visibility only. No runtime enforcement, job blocking, cron/config changes, MCP/toolkit wiring, account/public/paid/destructive actions, or new worker authority.",
        "source_report": "dashboard/policy_card_registry_summary.json",
        "registry": "policy_card_registry.json",
    }


def markdown(summary: dict[str, Any]) -> str:
    c = summary["counts"]
    lines = [
        "# Agent Policy Card Registry Summary — Report Only",
        "",
        f"Generated: {summary['generated_at']}",
        f"Mode: `{summary['mode']}`",
        f"Enforcement: `{summary['enforcement']}`",
        "",
        "> Visibility only. This summary does not grant authority, block jobs, alter cron/config, wire MCP/toolkits, or approve public/account/paid/destructive actions.",
        "",
        "## Counts",
        f"- OK cards: {c['ok_cards']}",
        f"- Missing cards: {c['missing_cards']}",
        f"- Stale cards: {c['stale_cards']}",
        f"- Validator failures: {c['validator_failures']}",
        "",
        "## Attention lanes",
    ]
    if not summary["attention_lanes"]:
        lines.append("- None.")
    else:
        for item in summary["attention_lanes"]:
            lines.append(f"- `{item['lane_id']}` — {', '.join(item['statuses'])}")
            lines.append(f"  - Card: `{item['policy_card_path']}`")
            lines.append(f"  - Next review due: `{item['next_review_due']}`")
            lines.append("  - Status: report-only visibility, not enforcement.")
    lines += [
        "",
        "## Source files",
        "- `policy_card_registry.json`",
        "- `check_policy_card_registry.py`",
        "- `dashboard/policy_card_registry_summary.json`",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate compact report-only policy-card registry dashboard summary.")
    parser.add_argument("--today", default=date.today().isoformat(), help="YYYY-MM-DD date for deterministic registry check")
    parser.add_argument("--json-out")
    parser.add_argument("--output", help="compatibility alias for --json-out")
    parser.add_argument("--md-out")
    args = parser.parse_args(argv)

    report = run_checker(args.today)
    summary = compact_summary(report)
    json_target = args.output or args.json_out or str(OUT_JSON)
    md_target = args.md_out
    if md_target is None and args.output is None:
        md_target = str(OUT_MD)

    json_out = Path(json_target)
    if not json_out.is_absolute():
        json_out = PROJECT_ROOT / json_out
    json_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json_out)
    if md_target is not None:
        md_out = Path(md_target)
        if not md_out.is_absolute():
            md_out = PROJECT_ROOT / md_out
        md_out.parent.mkdir(parents=True, exist_ok=True)
        md_out.write_text(markdown(summary), encoding="utf-8")
        print(md_out)
    print(json.dumps(summary["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
