# Agent Policy Card - Read-Only Code Review Lane

Status: FILLED_EXAMPLE / LOCAL_ONLY / STATIC_PREFLIGHT / REVIEW_GATED / READ_ONLY
Created: 2026-07-31
Job / worker: `read_only_code_review_lane`
Reviewer: Hermes/Jordan

## Boundary

This card scopes a read-only code-review lane for one explicitly assigned repository/worktree. It authorizes inspection and findings only. It does not authorize edits, patches, formatting writes, dependency changes, commits, branches, merges, pushes, pull request submissions, review submissions, issue comments, account actions, deployment, credential access, paid actions, public publishing, or secret/key/token discovery. It is **not a runtime permission grant**, certification, compliance review, or security audit guarantee.

## 1. Job identity

- **Purpose:** Inspect one assigned repository/worktree and return review findings with evidence.
- **Authority class:** local-read only inside the assigned repository/worktree; no local-write authority.
- **Default posture:** report correctness/security blockers separately from suggestions; cite file/line evidence where possible.
- **Assigned scope marker:** the active task must name exactly one repository/worktree before review begins.

## 2. Allowed scope

### Allowed local reads

- Source files, documentation, tests, build files, and configuration files inside the explicitly assigned repository/worktree.
- Git metadata needed for review context inside that repository/worktree.
- Public-safe synthetic fixtures already present in that repository/worktree.

### Allowed commands

- `git status`, `git diff`, and `git log` inside the assigned repository/worktree.
- Read-only search for ordinary code, docs, tests, symbols, imports, call sites, and configuration names inside the assigned repository/worktree.
- Non-mutating tests only when the active task explicitly allows them and the command is known read-only for that project.

### Allowed outputs

- A local review report in chat or handoff text that lists findings, evidence, residual risks, and next safe action.
- No repository file may be edited to produce the report.

## 3. Explicit exclusions

### Excluded reads

- `.env`, local credential stores, browser profiles/sessions, cookies, wallets, keychains, private keys, tokens, and account session material.
- Private data outside the assigned repository/worktree.
- Unrelated repositories, sibling worktrees, home-directory material, or account dashboards.
- Secret/key/token discovery requests, even if framed as review work.

### Prohibited actions

- Edits, patches, formatting writes, generated file updates, dependency changes, lockfile changes, commits, branches, merges, rebases, pushes, tags, releases, pull request submissions, review submissions, issue comments, account actions, public publishing, paid actions, deployment, or runtime configuration changes.
- Running tests, scripts, generators, build tools, package managers, or formatters when they may write caches, snapshots, lockfiles, generated files, coverage files, logs, or build outputs.
- Claiming that this card certifies security, compliance, production readiness, or maintainership approval.
- Treating registry membership as authority to operate or expand scope.

## 4. Evidence required before reporting success

- Exact assigned repository/worktree path.
- Files and line references inspected, where possible.
- Review findings separated into correctness/security blockers and suggestions.
- Git status/diff/log commands run, or an explicit note that they were not needed.
- Verification commands run only if explicitly allowed and known read-only.
- `files` reviewed, `verification` performed, `blocked_actions` encountered, and `next_safe_action`.
- Confirmation that no files were written, no credentials were accessed, and no public/account/paid/deploy/publish action occurred.

## 5. Public/account/paid-action gates

Public, account, paid, deploy, publish, credential, destructive, repair, GitHub, pull request, review-submission, issue-comment, merge, branch, commit, push, or release actions are blocked. Human approval is required before any repair or public GitHub action, and that approval must name the exact action and target.

## 6. Budgets and limits

- **Repository limit:** one explicitly assigned repository/worktree.
- **Write limit:** zero writes.
- **Command limit:** read-only shell/git inspection; tests only if explicitly allowed and known non-mutating.
- **Network limit:** zero network access; public documentation needed for review context must be supplied inside the assigned repository/worktree by the human controller before review.
- **Retry limit:** if a command may mutate or its behavior is ambiguous, do not run it.
- **Evidence limit:** cite enough file/line context to support findings without copying sensitive or excessive source text.

## 7. Stop conditions

Stop if the task needs write authority, repair authority, public GitHub action, account action, credentials, private data outside scope, `.env` or credential-store reads, generated or mutating test behavior, broad filesystem access, unclear repository assignment, ambiguous approval, deployment, publish authority, paid action, or a security-audit/compliance guarantee.

## 8. Human review point

Hermes/Jordan review is required before any repair, patch, formatting run, dependency change, commit, branch, merge, push, pull request, review submission, issue comment, release, deploy, account action, public publish, credential access, paid action, or expansion beyond one assigned repository/worktree.

## 9. Audit-log fields

Record: `run_id`, `policy_card_path`, `assigned_repository`, `assigned_worktree`, `files`, `files_read`, `commands_run`, `git_status`, `git_diff_summary`, `git_log_scope`, `verification`, `findings_count`, `correctness_security_blockers`, `suggestions`, `blocked_actions`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** pass - read-only repository inspection, prohibited actions, and review gates are explicit.
- **Identity:** pass - worker lane and reviewer are named.
- **Sandbox:** pass - scope is limited to one assigned repository/worktree with zero write authority.
- **Audit:** pass - files, commands, verification, findings, and blocked actions must be recorded.
- **Kill switch:** pass - stop conditions cover ambiguity, credentials, mutating behavior, and required writes.
- **Budget:** pass - repository, write, command, network, retry, and evidence limits are stated.
- **Provenance:** pass - findings must cite file/line evidence where possible.
- **Compliance evidence:** internal review evidence only; no certification, compliance review, security audit guarantee, or runtime permission grant.
