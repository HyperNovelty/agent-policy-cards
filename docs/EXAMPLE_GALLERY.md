# Example Gallery

This gallery summarizes the static example cards in `examples/`. The cards are
local, advisory, and review-gated. They do not grant runtime authority or approve
public/account/paid/destructive actions.

## Examples

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

## Regeneration

The gallery can be regenerated deterministically from the registry with:

```bash
python3 scripts/build_example_gallery.py
```

Use `--check` to verify the checked-in gallery is current.
