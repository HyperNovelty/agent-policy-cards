# Agent Policy Card - Bounded Issue Triage Lane

Status: FILLED_EXAMPLE / LOCAL_ONLY / STATIC_PREFLIGHT / REPORT_ONLY / REVIEW_GATED
Created: 2026-08-17
Job / worker: `bounded_issue_triage_lane`
Reviewer: Hermes/Jordan

## Boundary

This card scopes a static issue-triage lane for one explicitly assigned public-safe issue packet or one explicitly assigned repository issue context at a time. It authorizes local inspection and a draft triage recommendation only. It does not authorize GitHub comments, labels, assignments, milestones, state changes, closure, reopen actions, pull requests, patches, commits, pushes, account actions, deployment, credential access, paid actions, public publishing, outreach, or secret/key/token discovery. It is **not a runtime permission grant**, maintainer decision, SLA, security or compliance certification, or promise of resolution.

## 1. Job identity

- **Purpose:** Classify one supplied issue packet or one explicitly assigned repository issue context and draft a local triage report with evidence, uncertainty, and next safe action.
- **Authority class:** local-read and local-report only; no repository, GitHub, account, public, deployment, or implementation authority.
- **Default posture:** preserve `SOURCE_FACT`, `INTERPRETATION`, `RECOMMENDATION`, `DECISION`, and `ASSIGNMENT` as visibly distinct categories.
- **Assigned scope marker:** the active task must name exactly one issue packet or exactly one repository issue context before triage begins.

## 2. Allowed scope

### Allowed inputs

- Supplied public-safe issue title, body, comments, timestamps, labels, links, and reproduction notes when included in the assigned issue packet or explicitly assigned issue context.
- Repo-local `CONTRIBUTING.md`, `SECURITY.md`, issue templates, maintainer docs, release notes, changelog entries, and other public-safe process docs.
- Repo-local code, docs, tests, stack traces, logs, or git context only when the assigned packet explicitly includes those references.
- Public-safe synthetic fixtures already present in the assigned repository/worktree.

### Allowed local reads

- Files and git context inside the explicitly assigned repository/worktree when needed to evaluate the supplied issue context.
- Ordinary code, docs, tests, symbols, import paths, configuration names, and issue-template text referenced by the assigned packet.
- Existing local examples and fixtures that demonstrate triage categories or validator expectations.

### Allowed outputs

- A local triage report or draft recommendation in chat or a local review artifact when the current task explicitly requests a file.
- Evidence-backed fields for classification, severity rationale, duplicate/reproduction notes, missing evidence, uncertainty, and next safe action.
- Explicit category separation using `SOURCE_FACT`, `INTERPRETATION`, `RECOMMENDATION`, `DECISION`, and `ASSIGNMENT`.

## 3. Explicit exclusions

### Excluded inputs and reads

- Private issue/customer/security-report data unless the human controller has provided a public-safe synthetic or redacted packet for this lane.
- `.env`, credential stores, browser profiles/sessions, cookies, wallets, private keys, tokens, account session material, and private unrelated files.
- External GitHub/API/account access, private dashboards, external trackers, email, chat systems, or any source not included in the assigned issue packet or repo-local context.
- Secret/key/token discovery requests, even when framed as confirming impact.

### Prohibited actions

- Commenting on issues, adding/removing labels, assigning people, setting milestones, changing state, closing, reopening, creating pull requests, submitting reviews, or changing GitHub/account settings.
- Patches, implementation repair, formatting writes, generated file updates, dependency changes, commits, branches, merges, pushes, tags, releases, deployment, public publishing, outreach, paid actions, or credential access.
- Claiming that a maintainer decided, accepted, assigned, prioritized, scheduled, fixed, closed, or resolved anything without direct source evidence.
- Treating a `RECOMMENDATION` as a `DECISION` or `ASSIGNMENT`.
- Treating this card, registry membership, or validator success as runtime authority to operate or expand scope.

## 4. Evidence required before reporting success

- Exact assigned issue packet or repository issue context identifier.
- Source facts copied or summarized only from the supplied public-safe packet and allowed repo-local context.
- Classification with rationale, such as bug, feature request, documentation, question, duplicate candidate, security-sensitive report needing human handling, or insufficient evidence.
- Severity rationale and impact uncertainty, including what is known, inferred, and not established.
- Duplicate/reproduction notes, including exact references inspected and whether reproduction evidence is present, absent, or ambiguous.
- Missing evidence list and the next safe action, such as ask for reproduction steps, request affected version, route to maintainer review, or park as insufficient evidence.
- `files` or references inspected, `verification` performed, `blocked_actions` encountered, and `next_safe_action`.
- Confirmation that no GitHub/API/account mutation, code change, credential access, public publishing, paid action, deploy, or outreach occurred.

## 5. Public/account/paid-action gates

Public, account, paid, deploy, publish, credential, destructive, GitHub mutation, pull request, issue-comment, label, assignment, milestone, state-change, closure, reopen, implementation, commit, push, release, or outreach actions are blocked. Human approval is required before any later GitHub or implementation action, and that approval must name the exact action, target issue or repository, artifact, actor, and rollback or correction path.

## 6. Budgets and limits

- **Issue limit:** one explicitly assigned issue packet or repository issue context per triage pass.
- **Write limit:** zero writes unless the current task explicitly requests a local report artifact; never write code, generated outputs, commits, or GitHub state.
- **Network limit:** zero network or API access; any public context must be supplied inside the packet or repo-local files.
- **Evidence limit:** do not infer maintainer decisions, priority, assignment, acceptance, schedule, fix status, closure, or duplicate status beyond direct source facts.
- **Privacy limit:** use only synthetic, redacted, or public-safe content.
- **Retry limit:** if scope or evidence remains ambiguous after one clarification attempt, stop and report the blocker.

## 7. Stop conditions

Stop if the task lacks exactly one assigned issue packet or repository issue context; asks for GitHub/API/account mutation; needs external access; includes private data, credentials, or unredacted sensitive reports; requests implementation repair; requires secret/key/token discovery; has insufficient evidence to classify; conflates `RECOMMENDATION` with `DECISION` or `ASSIGNMENT`; or asks for public, paid, deploy, publish, outreach, closure, reopen, label, assignment, milestone, pull request, commit, push, or release action.

## 8. Human review point

Hermes/Jordan review is required before any GitHub comment, label, assignment, milestone, state change, close/reopen action, pull request, implementation patch, commit, branch, merge, push, release, deploy, account action, public publish, outreach, credential access, paid action, or expansion beyond one assigned issue context. Any later human approval must name the action and target; this card only supports a local recommendation.

## 9. Audit-log fields

Record: `run_id`, `started_at`, `ended_at`, `operator_or_agent`, `policy_card_path`, `assigned_issue_context`, `issue_packet_source`, `allowed_scope_used`, `files`, `references_read`, `source_facts`, `interpretations`, `recommendations`, `decisions_source_evidence`, `assignments_source_evidence`, `missing_evidence`, `severity_rationale`, `duplicate_notes`, `reproduction_notes`, `verification`, `blocked_actions`, `stop_condition_triggered`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** pass - report-only triage authority, prohibited actions, category separation, and human gates are explicit.
- **Identity:** pass - bounded_issue_triage_lane and Hermes/Jordan reviewer are named.
- **Sandbox:** pass - scope is limited to one assigned issue packet or repository issue context with zero GitHub/API/account mutation authority.
- **Audit:** pass - source facts, interpretations, recommendations, decisions evidence, assignments evidence, files, verification, blocked actions, and next safe action must be recorded.
- **Kill switch:** pass - stop conditions cover ambiguous scope, private data, credentials, external access, insufficient evidence, requested mutation, and category promotion.
- **Budget:** pass - issue, write, network, evidence, privacy, and retry limits are stated.
- **Provenance:** pass - triage findings must trace to supplied public-safe issue context or allowed repo-local references.
- **Compliance evidence:** internal review evidence only; no runtime permission grant, maintainer decision, SLA, security/compliance certification, or promise of resolution.
