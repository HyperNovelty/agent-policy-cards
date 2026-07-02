#!/usr/bin/env python3
"""Build the deterministic example gallery from the policy-card registry."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PROJECT_ROOT / "policy_card_registry.json"
GALLERY_PATH = PROJECT_ROOT / "docs" / "EXAMPLE_GALLERY.md"

DETAILS = {
    "codex_local_productization_lane": {
        "demonstrates": (
            "A bounded local coding/productization lane with assigned workspace "
            "scope, local tests or smoke checks, public-safe fixture discipline, "
            "and human-facing handoff evidence."
        ),
        "does_not_authorize": (
            "Public launch, credential or private-data access, account actions, "
            "global installs, paid services, broad filesystem access, or "
            "unattended production deployment."
        ),
    },
    "daily_ai_tool_scout": {
        "demonstrates": (
            "A recurring public-web-read and local-report workflow for reviewing "
            "AI/tool/governance signals without installing tools or changing "
            "runtime configuration."
        ),
        "does_not_authorize": (
            "Tool installation, MCP/server wiring, provider or cron changes, "
            "account login, public posting, publishing, email/social outreach, "
            "paid actions, or claims of compliance certification."
        ),
    },
    "future_source_to_system_promotion": {
        "demonstrates": (
            "A source-to-system promotion lane that converts vetted local source "
            "packets into review-only drafts, local artifacts, dashboard review "
            "items, or workflow notes while preserving provenance and review gates."
        ),
        "does_not_authorize": (
            "Publishing, source-backed readiness claims, account writes, public "
            "draft preload, recurring automation, credential access, paid actions, "
            "or deployment."
        ),
    },
    "ipublishos_dashboard_editor_patch": {
        "demonstrates": (
            "A narrow local dashboard/editor patch lane with scoped local reads "
            "and writes, generator runs, JSON/HTML/browser-local verification, "
            "and explicit review evidence."
        ),
        "does_not_authorize": (
            "Deploys, account sync, Google/Substack/KDP actions, credential "
            "access, third-party scripts or package installs without vetting, "
            "public publishing, or broad filesystem rewrites."
        ),
    },
}


def wrap_bullet(label: str, text: str) -> list[str]:
    return [f"- **{label}:** {text}"]


def build_gallery() -> str:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    lanes = sorted(registry["lanes"], key=lambda lane: lane["lane_id"])

    lines = [
        "# Example Gallery",
        "",
        "This gallery summarizes the static example cards in `examples/`. The cards are",
        "local, advisory, and review-gated. They do not grant runtime authority or approve",
        "public/account/paid/destructive actions.",
        "",
        "## Examples",
        "",
    ]

    for lane in lanes:
        lane_id = lane["lane_id"]
        detail = DETAILS.get(lane_id)
        if detail is None:
            raise KeyError(f"missing gallery detail for lane_id: {lane_id}")

        lines.extend(
            [
                f"### `{lane_id}`",
                "",
                f"- **Card:** `{lane['policy_card_path']}`",
                *wrap_bullet("Demonstrates", detail["demonstrates"]),
                *wrap_bullet("Does not authorize", detail["does_not_authorize"]),
                "",
            ]
        )

    lines.extend(
        [
            "## Intake Artifacts",
            "",
            "The repository also includes an AI Use Intake Card lane for capturing a",
            "public-safe workflow summary before deciding whether policy cards, authority",
            "envelopes, stronger evidence, or human review are needed.",
            "",
            "### `ai_use_intake_card`",
            "",
            "- **Schema:** `schemas/ai_use_intake_card.schema.json`",
            "- **Fixture:** `examples/ai_use_intake_card.customer_support_fixture.json`",
            "- **Rendered demo:** `examples/rendered/ai_use_intake_card_demo.md`",
            "- **Contract:** `docs/ai_use_intake_card_contract.md`",
            "- **Does not authorize:** Compliance approval, deployment approval, legal advice, certification, public/account actions, or permission to operate.",
            "",
            "## Regeneration",
            "",
            "The gallery can be regenerated deterministically from the registry with:",
            "",
            "```bash",
            "python3 scripts/build_example_gallery.py",
            "```",
            "",
            "Use `--check` to verify the checked-in gallery is current.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build docs/EXAMPLE_GALLERY.md")
    parser.add_argument("--check", action="store_true", help="fail if the gallery is out of date")
    args = parser.parse_args(argv)

    rendered = build_gallery()
    if args.check:
        existing = GALLERY_PATH.read_text(encoding="utf-8") if GALLERY_PATH.exists() else ""
        if existing != rendered:
            print(f"{GALLERY_PATH.relative_to(PROJECT_ROOT)} is out of date", file=sys.stderr)
            return 1
        print(f"{GALLERY_PATH.relative_to(PROJECT_ROOT)} is current")
        return 0

    GALLERY_PATH.parent.mkdir(parents=True, exist_ok=True)
    GALLERY_PATH.write_text(rendered, encoding="utf-8")
    print(f"wrote {GALLERY_PATH.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
