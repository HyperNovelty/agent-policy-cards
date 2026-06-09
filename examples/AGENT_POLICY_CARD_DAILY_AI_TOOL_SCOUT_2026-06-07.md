# Agent Policy Card — Daily AI Tool Scout

Status: FILLED_EXAMPLE / LOCAL_ONLY / REVIEW_GATED  
Created: 2026-06-07  
Job / worker: `daily_ai_tool_scout`  
Reviewer: Jordan / Hermes  
Source pattern: Microsoft Agent Governance Toolkit categories; GitHub Copilot sandbox/planning signal; existing Hypernovelty no-public-action gates

**Boundary:** local/static documentation only. This card is not a runtime permission grant, not an install instruction, not a policy engine, not a legal/compliance claim, and not approval for public/account/paid/destructive actions.

## 1. Job identity

- **Purpose:** Find a small number of current AI/tool/governance signals and convert only the best one into a safe local next experiment for Hypernovelty.
- **Authority class:** network-read + local-write only.
- **Default posture:** may read public web sources and local state files; may write reports/state notes; may not install, connect, publish, post, spend, or change runtime configuration.

## 2. Allowed scope

### Allowed local reads

- `reports/daily_ai_tool_scout/`
- `ops/AI_TOOL_SCOUT_STATE.md`
- `products/agent_os_authority_layer/` documentation/templates/index/queue
- relevant local review packets under `reports/tool_vetting/` when explicitly tied to tool governance

### Allowed local writes

- `reports/daily_ai_tool_scout/YYYY-MM-DD_daily_ai_tool_scout.md`
- `ops/AI_TOOL_SCOUT_STATE.md`
- review-gated Agent OS artifacts under:
  - `products/agent_os_authority_layer/templates/`
  - `products/agent_os_authority_layer/examples/`
  - `reports/tool_vetting/`

### Allowed external/network reads

- Public documentation, changelog, blog, arXiv, and GitHub repository pages relevant to AI agents/tools/governance.
- Public metadata APIs only when no credentials are required.

### Allowed tools/actions

- Web search/extract/read-only public browsing.
- Local file reads/searches in allowed project paths.
- Local Markdown/HTML artifact creation.
- Local validation: path existence, JSON parse, marker checks, size checks, link/source presence checks.

## 3. Explicit exclusions

### Excluded local reads

- `.env`, credential files, token files, private keys, browser profiles/sessions, wallet/broker/exchange/payment material.
- Private inboxes/account dashboards unless the active task explicitly says to process that inbox and the skill/gate allows it.
- Unrelated personal folders outside `/home/aware1/.hermes/content-empire`.

### Prohibited actions

- Installing Microsoft Agent Governance Toolkit or any candidate repo/tool.
- Connecting MCP servers, changing Hermes config, editing cron schedules, or changing providers/models.
- Publishing, posting, emailing, DMing, uploading, deploying, creating accounts, logging into accounts, changing settings, submitting forms, buying tools/domains, or spending money.
- Running untrusted repo code.
- Claiming compliance, security certification, or legal sufficiency.
- Broadly agentifying arbitrary software or exposing private/source-vault surfaces.

## 4. Evidence required before reporting success

- Report path exists and is non-empty.
- State/index updates, if performed, exist and include the chosen recommendation marker.
- Every created card includes: purpose, allowed scope, exclusions, allowed actions, prohibited actions, evidence, gates, budgets, stop conditions, human review, and audit fields.
- Final summary lists blockers vs warnings and the next safe action.
- No install/config/runtime/account/public action occurred.

## 5. Public/account/paid-action gates

Blocked unless Jordan explicitly approves the exact action: public posting/publishing/email/social; KDP/Substack/Google/GitHub/account changes; DNS/cloud/deploy/analytics/form connections; paid tools/subscriptions/purchases/credits; credential inspection or secret handling; outreach/applications/submissions/legal/tax/financial actions.

## 6. Budgets and limits

- **Time limit:** 20–30 minutes for the scout and policy-card test.
- **External source limit:** prefer 3–7 high-signal sources; no account-gated sources.
- **Install/runtime limit:** zero.
- **Output limit:** one daily report plus at most one promoted static template/example pair.
- **Retry limit:** if verification fails twice, stop and report the blocker.

## 7. Stop conditions

Stop if the scout requires a package install/repo execution; secrets/auth/account dashboards/browser sessions/credentials; public/account/paid/destructive action; more authority than local read/write and public web read; or uncertain source status that would turn the recommendation into a claim beyond evidence.

## 8. Human review point

Jordan/Hermes review is required before making the card a required template for recurring jobs; wiring it into dashboard controls or cron prompts; turning static fields into runtime enforcement; or using Microsoft Agent Governance Toolkit code/packages directly.

Decision options: Approve static reuse / Needs changes / Park / Reject / Promote proposal.

## 9. Audit-log fields for each run

```json
{
  "run_id": "daily_ai_tool_scout_YYYY-MM-DD",
  "policy_card_path": "products/agent_os_authority_layer/examples/AGENT_POLICY_CARD_DAILY_AI_TOOL_SCOUT_2026-06-07.md",
  "started_at": "ISO-8601",
  "ended_at": "ISO-8601",
  "sources_read": [],
  "local_files_read": [],
  "files_created_or_modified": [],
  "tools_used": [],
  "verification_results": [],
  "blocked_actions_encountered": [],
  "stop_condition_triggered": false,
  "human_review_needed": true,
  "next_safe_action": "static reuse or runtime-enforcement proposal"
}
```

## 10. Governance category map

- **Policy:** pass — exact permissions, prohibitions, gates, and stop conditions are stated.
- **Identity:** partial/pass — job name and reviewer are named; stronger identity would require a worker registry entry.
- **Sandbox:** partial — local paths are scoped, but this is not an execution sandbox. If code execution is added, use a disposable sandbox/worktree/container.
- **Audit:** pass — required evidence and audit fields are explicit.
- **Kill switch:** pass for static operation — stop conditions are clear; runtime kill switch would need separate implementation.
- **Budget:** pass — time/source/install/output/retry limits are explicit.
- **Provenance:** pass — sources/local files/output paths must be recorded.
- **Compliance evidence:** limited — useful as internal evidence discipline only; no certification/legal claim.
