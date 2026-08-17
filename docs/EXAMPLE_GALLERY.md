# Example Gallery

This gallery summarizes the static example cards in `examples/`. The cards are
local, advisory, and review-gated. They do not grant runtime authority or approve
public/account/paid/destructive actions.

## Examples

### `bounded_issue_triage_lane`

- **Card:** `examples/AGENT_POLICY_CARD_BOUNDED_ISSUE_TRIAGE_LANE_2026-08-17.md`
- **Demonstrates:** A single-issue report-only triage lane that inspects supplied public-safe issue context, separates source facts from interpretations, recommendations, decisions, and assignments, and reports severity rationale, uncertainty, missing evidence, duplicate/reproduction notes, and next safe action.
- **Does not authorize:** GitHub/API integration, issue comments, labels, assignments, milestones, state changes, closure/reopen, pull requests, patches, commits, pushes, account actions, credential or private-data access, secret/key/token discovery, deployment, publishing, outreach, paid actions, or maintainer decision claims.

### `codex_local_productization_lane`

- **Card:** `examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md`
- **Demonstrates:** A bounded local coding/productization lane with assigned workspace scope, local tests or smoke checks, public-safe fixture discipline, and human-facing handoff evidence.
- **Does not authorize:** Public launch, credential or private-data access, account actions, global installs, paid services, broad filesystem access, or unattended production deployment.

### `daily_ai_tool_scout`

- **Card:** `examples/AGENT_POLICY_CARD_DAILY_AI_TOOL_SCOUT_2026-06-07.md`
- **Demonstrates:** A recurring public-web-read and local-report workflow for reviewing AI/tool/governance signals without installing tools or changing runtime configuration.
- **Does not authorize:** Tool installation, MCP/server wiring, provider or cron changes, account login, public posting, publishing, email/social outreach, paid actions, or claims of compliance certification.

### `future_source_to_system_promotion`

- **Card:** `examples/AGENT_POLICY_CARD_SOURCE_TO_SYSTEM_PROMOTION_LANE_2026-06-07.md`
- **Demonstrates:** A source-to-system promotion lane that converts vetted local source packets into review-only drafts, local artifacts, dashboard review items, or workflow notes while preserving provenance and review gates.
- **Does not authorize:** Publishing, source-backed readiness claims, account writes, public draft preload, recurring automation, credential access, paid actions, or deployment.

### `ipublishos_dashboard_editor_patch`

- **Card:** `examples/AGENT_POLICY_CARD_IPUBLISHOS_DASHBOARD_EDITOR_PATCH_2026-06-07.md`
- **Demonstrates:** A narrow local dashboard/editor patch lane with scoped local reads and writes, generator runs, JSON/HTML/browser-local verification, and explicit review evidence.
- **Does not authorize:** Deploys, account sync, Google/Substack/KDP actions, credential access, third-party scripts or package installs without vetting, public publishing, or broad filesystem rewrites.

### `read_only_code_review_lane`

- **Card:** `examples/AGENT_POLICY_CARD_READ_ONLY_CODE_REVIEW_LANE_2026-07-31.md`
- **Demonstrates:** A single-repository read-only code review lane with source/docs/test/config inspection, git status/diff/log context, evidence-backed findings, and explicit stop conditions for ambiguity or mutation.
- **Does not authorize:** Edits, patches, formatting writes, dependency changes, commits, branches, merges, pushes, PR/review submissions, issue comments, secret/key/token discovery, account actions, deploys, publishing, paid actions, or security/compliance certification claims.

## Intake Artifacts

The repository also includes an AI Use Intake Card lane for capturing a
public-safe workflow summary before deciding whether policy cards, authority
envelopes, stronger evidence, or human review are needed.

### `ai_use_intake_card`

- **Schema:** `schemas/ai_use_intake_card.schema.json`
- **Fixture:** `examples/ai_use_intake_card.customer_support_fixture.json`
- **Rendered demo:** `examples/rendered/ai_use_intake_card_demo.md`
- **Contract:** `docs/ai_use_intake_card_contract.md`
- **Does not authorize:** Compliance approval, deployment approval, legal advice, certification, public/account actions, or permission to operate.

## Regeneration

The gallery can be regenerated deterministically from the registry with:

```bash
python3 scripts/build_example_gallery.py
```

Use `--check` to verify the checked-in gallery is current.
