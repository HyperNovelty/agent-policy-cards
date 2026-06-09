# Agent Policy Card — Codex Local Productization Lane

Status: FILLED_EXAMPLE / LOCAL_ONLY / STATIC_PREFLIGHT / REVIEW_GATED  
Created: 2026-06-07  
Job / worker: `codex_local_productization_lane`  
Reviewer: Jordan / Hermes  

## Boundary

This card scopes a bounded local Codex-style build lane for Hypernovelty productization. It does not authorize public launch, paid services, external account actions, credentials, broad filesystem access, or unattended production deployment. It is **not a runtime permission grant** and cannot be used to auto-authorize tools.

## 1. Job identity

- **Purpose:** Build or improve one local reviewable product/workflow artifact from an approved HN plan, with tests or smoke checks and a human-facing handoff.
- **Authority class:** local-read + local-write + local-code-execution inside an approved workspace. Network access only if the active task explicitly allows public docs/package metadata reads.
- **Default posture:** use the narrowest workspace; no source-vault/account/private data access unless explicitly included in the task and card.

## 2. Allowed scope

### Allowed local reads

- The active plan/handoff file named by Hermes/Jordan.
- The assigned workspace under `products/`, `content-empire/sandboxes/`, or another explicitly named HN project folder.
- Relevant project-local docs/fixtures/tests required for the assigned build.
- Public-safe synthetic fixtures created for the lane.

### Allowed local writes

- Files inside the assigned workspace only.
- Local reports/handoffs under `reports/`, `operations/automode/`, or the workspace `docs/` folder.
- Windows review packet copies when explicitly requested or useful for Jordan review.

### Allowed external/network reads

- Public documentation and package metadata necessary to understand an already-approved local build.
- No account-gated docs, private repos, API-key endpoints, paid services, or live customer/client data.

### Allowed tools/actions

- Local code edits in the assigned workspace.
- Local tests, linters, validators, build scripts, and smoke checks.
- Git status/diff/log in the assigned workspace if it is a repo.
- Local artifact generation: Markdown, HTML, JSON, CSV, screenshots only when safe/local.

## 3. Explicit exclusions

### Excluded reads

- `.env`, token/secret/key files, browser profiles/sessions, cookies, wallets, payment/broker/exchange material.
- Private customer/client/medical/legal/financial/HR records.
- Unrelated HN folders outside the assigned workspace unless the plan explicitly names them.
- Account dashboards for KDP/Substack/Google/GitHub/X/Cloudflare/etc.

### Prohibited actions

- Publishing, posting, emailing, DMing, uploading, deploying, submitting, buying, subscribing, or changing account settings.
- Installing global packages or system services.
- Running untrusted repo code outside a disposable sandbox/workspace.
- Modifying Hermes config, providers, cron jobs, plugins, credentials, shell profiles, or system startup files.
- Deleting/moving files outside the assigned workspace.
- Using real sensitive data in demos or fixtures.
- Claiming production readiness without passing stated tests/smokes and human review gates.

## 4. Evidence required before reporting success

- Exact workspace path.
- Files created/edited.
- Test/build/smoke command output or explicit note if not applicable.
- Git status/diff summary when inside a repo.
- Human-facing review path, preferably Windows-openable if Jordan must inspect it.
- Known blockers/warnings and next safe action.
- Confirmation that no public/account/paid/credential/destructive action occurred.

## 5. Public/account/paid-action gates

Every public/account/paid/credential/destructive action requires separate explicit Jordan approval for the exact action and target. Productization work may prepare local artifacts and approval packets only.

## 6. Budgets and limits

- **Time limit:** bounded by the active task or automode window.
- **Workspace limit:** assigned folder only.
- **Network limit:** public docs/metadata only when useful; no account-gated or credentialed network.
- **Install limit:** no global installs; dependency changes must be local and justified by the active task.
- **Retry limit:** if build/test fails twice from the same cause, stop and report blocker with logs.

## 7. Stop conditions

Stop if the lane needs credentials, private data, public launch, account actions, cloud/DNS, paid tools, broad filesystem access, destructive cleanup outside workspace, ambiguous source authority, or a dependency/install path that expands risk beyond the card.

## 8. Human review point

Jordan/Hermes review is required before promoting the local artifact to public website, Substack/KDP/Google, customer-facing demo, paid product, production workflow, account-connected automation, or recurring worker.

## 9. Audit-log fields

Record: `run_id`, `policy_card_path`, `assigned_workspace`, `plan_source`, `files_read`, `files_written`, `commands_run`, `test_results`, `verification_results`, `artifact_paths`, `git_status`, `blocked_actions`, `rollback_notes`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** pass — workspace, actions, exclusions, and gates are explicit.
- **Identity:** pass — worker lane and reviewer named.
- **Sandbox:** partial/pass — assigned workspace required; disposable sandbox required for untrusted code.
- **Audit:** pass — command/file/test/handoff evidence required.
- **Kill switch:** pass — stop conditions and retry limits are explicit.
- **Budget:** pass — workspace/network/install/retry limits stated.
- **Provenance:** pass — plan source and artifacts must be recorded.
- **Compliance evidence:** internal evidence only; no certification/legal/compliance claim.
