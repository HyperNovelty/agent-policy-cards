# Agent Policy Card Template — Local Only

Status: TEMPLATE / LOCAL_ONLY / REVIEW_GATED  
Created: 2026-06-07  
Lane: Agent OS / Authority Layer  
Source pattern: Microsoft Agent Governance Toolkit signal review + existing Hypernovelty authority-layer templates

**Boundary:** local/static documentation only. This card is not a runtime permission grant, not an install instruction, not a policy engine, not a legal/compliance claim, and not approval for public/account/paid/destructive actions.

## 1. Job identity

- **Job / worker name:** `<short stable name>`
- **Owner / reviewer:** Jordan / Hermes / named operator
- **Purpose in one sentence:** `<what useful outcome this worker exists to produce>`
- **Authority class:** Read-only / local-write / code-execution / network-read / account-action / public-action
- **Default posture:** deny by default outside this card

## 2. Allowed scope

- **Allowed folders/files:** `<exact local/project-relative paths>`
- **Allowed inputs:** `<approved source files, reports, URLs, local packets, synthetic fixtures>`
- **Allowed outputs:** `<exact destination folder and artifact type>`
- **Allowed tools/actions:** `<search/read/write/test/web-read/etc.>`

## 3. Explicit exclusions

- **Excluded folders/files:** `.env`, credentials, tokens, private keys, browser profiles/sessions, payment/account material, unrelated personal/private folders.
- **Prohibited actions:** publish/post/email/DM/upload/deploy/share; account/settings/login changes; spending/subscriptions/domain purchases/form submissions; credential inspection; destructive moves/deletes outside disposable sandboxes; self-modifying this policy or widening authority.

## 4. Evidence required before reporting success

- Exact created/edited file paths.
- Files exist and are non-empty.
- Key strings/sections are present.
- Verification command/check passes: `<test, validator, source ledger check, JSON parse, link check, human review>`.
- Diff/rollback note says what changed and how to reverse if needed.

## 5. Public/account/paid-action gates

All public, account, credential, paid, DNS/cloud, outreach, upload, publishing, legal/tax, financial, KDP/Substack/Google/social, or deployment actions are **blocked until explicit current human approval** for the exact action, target, artifact, and rollback plan.

## 6. Budgets and limits

- **Time limit:** `<e.g. 20–30 minutes>`
- **Browse/network limit:** `<allowed domains or no network>`
- **Token/cost limit:** `<if known; otherwise no paid actions>`
- **Retry limit:** `<max attempts before stop>`
- **Output limit:** `<number/type of artifacts>`

## 7. Stop conditions

Stop immediately if the task requires credentials/secrets/account login; would publish/send/deploy/spend/submit/delete/change public or account settings; expands beyond listed folders; has insufficient/conflicting sources; fails verification after retry limit; or a tool requests broader authority than this card grants.

## 8. Human review point

- **Review required when:** `<before install/runtime wiring/public use/workflow promotion>`
- **Reviewer decision options:** Approve static reuse / Needs changes / Park / Reject / Promote to runtime enforcement proposal

## 9. Audit-log fields

Record at minimum: `run_id`, `started_at`, `ended_at`, `operator_or_agent`, `policy_card_path`, `allowed_scope_used`, `tools_used`, `files_created_or_modified`, `sources_read`, `verification_results`, `blocked_actions_encountered`, `stop_condition_triggered`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** card names permissions, prohibitions, gates, stop conditions.
- **Identity:** worker/job and reviewer are explicit.
- **Sandbox:** workspace/output folders are scoped; execution sandbox required for code-running lanes.
- **Audit:** evidence and audit fields are listed.
- **Kill switch:** stop conditions define halt points.
- **Budget:** time/network/retry/output limits are explicit.
- **Provenance:** inputs/sources and output paths are captured.
- **Compliance evidence:** local evidence discipline only; no certification/legal claim.
