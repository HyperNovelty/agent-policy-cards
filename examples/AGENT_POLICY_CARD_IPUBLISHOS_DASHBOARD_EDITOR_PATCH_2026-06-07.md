# Agent Policy Card — iPublishOS Dashboard Editor Patch

Status: FILLED_EXAMPLE / LOCAL_ONLY / STATIC_PREFLIGHT / REVIEW_GATED  
Created: 2026-06-07  
Job / worker: `iPublishOS_dashboard_editor_patch`  
Reviewer: Jordan / Hermes  

## Boundary

This card scopes a local dashboard/editor patch lane. It is not permission to deploy, publish, edit accounts, connect Google/Substack/KDP, inspect credentials, or change Hermes runtime/cron/provider settings. It is **not a runtime permission grant** and cannot be used to auto-authorize tools.

## 1. Job identity

- **Purpose:** Make a bounded local patch to the iPublishOS / Hypernovelty dashboard or editor so Jordan can review a safer or clearer local cockpit/workflow.
- **Authority class:** local-read + local-write + local-test. No account, deploy, public, paid, credential, or cloud authority.
- **Default posture:** deny by default outside exact files named in the active task and this card.

## 2. Allowed scope

### Allowed local reads

- `dashboard/` files directly related to the active patch.
- `dashboard/operator_status.json` and `dashboard/command_center_tasks.snapshot.json` for status/queue context.
- `products/agent_os_authority_layer/` templates/index/queue when the patch concerns governance cards.
- `operations/automode/` or `reports/tool_vetting/` only when linked by the active task.

### Allowed local writes

- The specifically named dashboard/editor files in the active task.
- New local review notes under `reports/tool_vetting/` or `operations/automode/`.
- Windows review copies under `C:\Users\Aware1\Desktop\Files for Hermes\Dashboard Designs\` when the output is meant for Jordan review.

### Allowed tools/actions

- Read/search project files.
- Write local HTML/JS/CSS/JSON/Markdown artifacts.
- Run deterministic local generators/tests/validators already present in the repo.
- Regenerate local dashboards after a data/status change.
- Verify JSON parse, file existence, marker strings, and local HTML generation.

## 3. Explicit exclusions

### Excluded reads

- `.env`, secrets, tokens, browser sessions/profiles, account cookies, payment files, private keys.
- Google/Substack/KDP/GitHub/X/cloud account dashboards unless a separate approval explicitly authorizes the exact account action.
- Unrelated personal/private folders outside `/home/aware1/.hermes/content-empire`.

### Prohibited actions

- Public deploys or DNS/cloud changes.
- Publishing, posting, emailing, uploading, or sharing.
- Account login, settings changes, integrations, webhooks, paid services, subscriptions, or form submissions.
- Installing packages or adding third-party scripts/CDNs without a separate vetting step.
- Deleting/moving source files except disposable generated outputs explicitly named by the active task.
- Modifying this card to broaden the running worker's own authority.

## 4. Evidence required before reporting success

- List exact files created/edited.
- JSON files parse successfully.
- Generated dashboard HTML exists in both project and Windows review path when applicable.
- Key visible marker appears in generated dashboard, not only raw JSON.
- Any interactive behavior changed must be tested by script or browser; if not tested, label as unverified.
- No public/account/runtime/config action occurred.

## 5. Public/account/paid-action gates

Blocked unless Jordan explicitly approves the exact action: Cloudflare/Pages deploy, DNS, analytics, forms, Substack/KDP/Google/X/GitHub account changes, public uploads/posts, social/email sends, paid services, credential inspection, legal/tax/financial actions.

## 6. Budgets and limits

- **Time limit:** one bounded patch pass unless Jordan asks for an automode sprint.
- **Write limit:** only named files plus review/report artifacts.
- **Dependency limit:** no new package installs by default.
- **Retry limit:** two regeneration/verification attempts before reporting blocker.

## 7. Stop conditions

Stop if the patch requires credentials, live account access, deploy/public action, third-party install, broad dashboard rewrite beyond the requested patch, destructive file operations, or unverified behavior that would be represented as working.

## 8. Human review point

Jordan review is required before using the patch as the default production path, connecting it to accounts, making public-visible changes, or adding stronger persistence/sync/export authority.

## 9. Audit-log fields

Record: `run_id`, `policy_card_path`, `task_summary`, `files_read`, `files_written`, `commands_run`, `generated_paths`, `json_parse_result`, `html_marker_check`, `interactive_test_result`, `blocked_actions`, `next_safe_action`.

## 10. Governance category map

- **Policy:** pass — exact local dashboard patch authority and prohibitions stated.
- **Identity:** pass — job/reviewer named.
- **Sandbox:** partial — scoped project/Windows review paths; stronger sandbox needed for untrusted code.
- **Audit:** pass — file/command/verification evidence required.
- **Kill switch:** pass — stop conditions explicit.
- **Budget:** pass — time/write/dependency/retry limits stated.
- **Provenance:** pass — dashboard/status/report source paths must be listed.
- **Compliance evidence:** internal operational evidence only; no compliance certification.
