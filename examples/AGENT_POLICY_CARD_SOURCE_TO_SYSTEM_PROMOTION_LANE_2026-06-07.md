# Agent Policy Card — Source-to-System Promotion Lane

Status: LOCAL_ONLY / STATIC_PREFLIGHT / REPORT_ONLY  
Created: 2026-06-07  
Lane: Agent OS / Authority Layer / iPublishOS source-to-system promotion  
Registry lane: `future_source_to_system_promotion`

**Boundary:** This card is local/static documentation only. It is **not a runtime permission grant**, not a job router, not cron wiring, not MCP wiring, not a toolkit install instruction, not a policy engine, and not approval for public/account/paid/destructive actions.

## 1. Job identity

- **Job / worker name:** source_to_system_promotion_lane
- **Owner / reviewer:** Jordan / Hermes review
- **Purpose in one sentence:** Convert a vetted local source packet or signal review into a clearly labeled local draft, product artifact, dashboard review item, or reusable workflow note without public/account actions.
- **Authority class:** local-write plus optional public/network-read only when the source packet explicitly requires verification; no account-action and no public-action authority.
- **Default posture:** deny by default outside this card.

## 2. Allowed scope

- **Allowed folders/files:**
  - `reports/`
  - `content/social_substack/`
  - `products/agent_os_authority_layer/`
  - `products/ipublishos_source_research_intake/`
  - `content_library/`
  - `dashboard/operator_status.json`
  - `dashboard/command_center.html`
  - `dashboard/command_center_tasks.snapshot.json`
  - Windows review copies under `C:\Users\Aware1\Downloads\` or `C:\Users\Aware1\Desktop\Files for Hermes\Dashboard Designs\` when created by the local dashboard/review workflow.
- **Allowed inputs:** local source packets, daily signal reviews, link-intake reports, source notes, public URLs already present in a packet, synthetic fixtures, and Jordan-provided links/comments.
- **Allowed outputs:** local Markdown/JSON/HTML review artifacts, source ledgers, draft packets labeled review-only, policy/worksheet/product-prep notes, and Command Center review cards.
- **Allowed tools/actions:** read local files, write local review artifacts, run validators, parse JSON, regenerate local Command Center, perform public web-read verification only for already supplied public source URLs, and produce evidence logs.

## 3. Explicit exclusions

- **Excluded folders/files:** `.env`, credentials, tokens, private keys, browser profiles/sessions, wallets, payment/account material, unrelated personal/private folders, raw private transcripts unless the current user request explicitly routes them into a local packet, and any path outside the scoped Hypernovelty project/review folders.
- **Prohibited actions:** publish, post, email, DM, upload, deploy, share, schedule, submit forms, change account settings, log in to accounts, inspect credentials, spend money, buy domains, alter DNS/cloud, preload Substack/KDP/Google/account drafts, perform destructive moves/deletes outside disposable sandboxes, widen this policy, or grant runtime authority.

## 4. Evidence required before reporting success

- Exact created/edited file paths.
- Files exist and are non-empty.
- Key strings/sections are present: source status, allowed scope, review-only/public-action gate, blockers vs warnings, and next safe action.
- Verification command/check passes: relevant JSON parse, Agent Policy Card validator if a card is created, source ledger/source-status check for source-backed artifacts, local link/path check, and Command Center regeneration when dashboard status is edited.
- Diff/rollback note says what changed and how to reverse or park the artifact if needed.
- `verification_results` must be recorded in the final handoff/report.

## 5. Public/account/paid-action gates

All public, account, credential, paid, DNS/cloud, outreach, upload, publishing, legal/tax, financial, KDP/Substack/Google/social, deployment, or form-submission actions are **blocked until explicit current human approval** for the exact action, target, artifact, and rollback plan.

A source-to-system promotion may prepare local review copy, local draft packets, local product notes, or local dashboard cards. It may not publish, preload, submit, deploy, send, or contact anyone.

## 6. Budgets and limits

- **Time limit:** 20–45 minutes per promotion pass unless Jordan gives an explicit longer automode window.
- **Browse/network limit:** public web-read only for source URLs already present in the source packet or user message; no account browsing and no scraping private dashboards.
- **Token/cost limit:** no paid actions or paid API/tool adoption; use existing configured local/Hermes tools only.
- **Retry limit:** one retry after a validation or path failure, then report blocker/warning.
- **Output limit:** one primary local artifact plus one compact status/handoff update unless the lane explicitly requires a packet set.

## 7. Stop conditions

Stop immediately if the task requires credentials/secrets/account login; would publish/send/deploy/spend/submit/delete/change public or account settings; expands beyond listed folders; needs private/sensitive material not already approved for the lane; has insufficient/conflicting sources; fails verification after retry limit; or a tool requests broader authority than this card grants.

## 8. Human review point

- **Review required when:** before public use, source-backed readiness claims, article marked review-ready, Substack/KDP/Google/account preload, workflow promotion to recurring automation, runtime enforcement, install, MCP/toolkit wiring, or any public/account/paid/destructive action.
- **Reviewer decision options:** Approve static reuse / Needs changes / Park / Reject / Promote to runtime enforcement proposal.

## 9. Audit-log fields

Record at minimum: `run_id`, `started_at`, `ended_at`, `operator_or_agent`, `policy_card_path`, `allowed_scope_used`, `tools_used`, `files_created_or_modified`, `sources_read`, `verification_results`, `blocked_actions_encountered`, `stop_condition_triggered`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** this card names permissions, prohibitions, gates, stop conditions, and required evidence.
- **Identity:** source_to_system_promotion_lane and Jordan/Hermes reviewer are explicit.
- **Sandbox:** workspace/output folders are scoped to local Hypernovelty project and Windows review copies.
- **Audit:** evidence and audit fields are listed, including `verification_results` and `policy_card_path`.
- **Kill switch:** stop conditions define halt points for credentials, accounts, public actions, scope expansion, or failed verification.
- **Budget:** time, network, retry, cost, and output limits are explicit.
- **Provenance:** inputs/sources and output paths must be captured in every promoted artifact.
- **Compliance evidence:** local evidence discipline only; no certification, legal, tax, medical, financial, or professional compliance claim.
