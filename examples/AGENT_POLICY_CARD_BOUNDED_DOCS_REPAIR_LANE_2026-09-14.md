# Agent Policy Card - Bounded Documentation Repair Lane

Status: FILLED_EXAMPLE / LOCAL_ONLY / STATIC_PREFLIGHT / REVIEW_GATED / DOCS_ONLY
Created: 2026-09-14
Job / worker: `bounded_docs_repair_lane`
Reviewer: Hermes/Jordan

## Boundary

This card scopes a bounded documentation-repair lane for one explicitly assigned repository/worktree. The active task must name the assigned repository/worktree with a repo-local or synthetic path such as `assigned-repo/`; do not embed private home-directory paths. It authorizes local documentation edits and a local repair report only. It does not authorize product source changes, product test changes, schema/script behavior changes, dependency or lockfile changes, CI/workflow changes outside Markdown comments, commits, branches, merges, pushes, tags, releases, pull request submissions, issue comments, account actions, deployment, credential access, paid actions, public publishing, GitHub Pages, or secret/key/token discovery. It is **not a runtime permission grant**, security/compliance certification, or permission to ship.

## 1. Job identity

- **Purpose:** Repair stale, missing, contradictory, or unclear documentation inside one assigned repository/worktree while keeping docs accurate to the existing source.
- **Authority class:** local-read plus documentation-only local-write inside the assigned repository/worktree.
- **Default posture:** keep repairs minimal, public-safe, reviewable, and tied to evidence already present in the assigned repository/worktree.
- **Assigned scope marker:** the active task must name exactly one repository/worktree before documentation repair begins.

## 2. Allowed scope

### Allowed local reads

- Source files, documentation, tests, schemas, scripts, build files, and configuration files inside the explicitly assigned repository/worktree, only as needed to keep documentation accurate.
- Git metadata needed for local repair context inside that repository/worktree.
- Public-safe synthetic fixtures already present in that repository/worktree.
- Existing reviewer-facing Markdown needed to avoid contradictory or duplicate documentation.

### Allowed local writes

- Documentation files only: `README.md`, `CHANGELOG.md`, `docs/`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `MAINTAINERS.md`, and other reviewer-facing Markdown already in the assigned repository/worktree.
- A local documentation repair report that lists files changed, verification, residual risks, blocked actions, and next safe action.

### Allowed commands

- Read source, documentation, tests, schemas, scripts, build files, and configuration files inside the assigned repository/worktree as needed to keep documentation accurate.
- Run existing documentation generators or documentation checks only when they are known to be scoped to documentation outputs.
- `git status`, `git diff`, and `git log` inside the assigned repository/worktree.
- Local validation commands for documentation files when the active task names them and they do not install dependencies, contact accounts, or write product outputs.

### Allowed outputs

- Local documentation edits inside the allowed documentation paths.
- A local repair report with files changed, verification performed, residual risks, blocked actions, and next safe action.

## 3. Explicit exclusions

### Excluded reads

- `.env`, local credential stores, browser profiles/sessions, cookies, wallets, keychains, private keys, tokens, account session material, and credential files.
- Private data outside the assigned repository/worktree.
- Unrelated repositories, sibling worktrees, home-directory material, or account dashboards.
- Secret/key/token discovery requests, even if framed as documentation cleanup.

### Prohibited actions

- Product source changes, product test changes, schema behavior changes, script behavior changes, dependency changes, lockfile changes, or generated product-output changes.
- CI/workflow changes, except documentation comments inside Markdown files.
- Commits, branches, merges, rebases, pushes, tags, releases, pull request submissions, review submissions, issue comments, GitHub Pages, account actions, public publishing, paid actions, deployment, or runtime configuration changes.
- Copying private paths, credential-like strings, or secret-like material into documentation.
- Claiming that this card certifies security, compliance, production readiness, maintainership approval, or permission to ship.
- Treating registry membership as authority to operate or expand scope.

## 4. Evidence required before reporting success

- Exact assigned repository/worktree path.
- Files read and files changed.
- Documentation repair summary tied to existing repository evidence.
- Git status/diff/log commands run, or an explicit note that they were not needed.
- Documentation generator/check commands run, or an explicit note that no scoped documentation check was applicable.
- `files` changed, `verification` performed, `blocked_actions` encountered, residual risks, and `next_safe_action`.
- Confirmation that no product source/test/schema/script behavior changed, no dependency or lockfile changed, no credentials were accessed, and no public/account/paid/deploy/publish action occurred.

## 5. Public/account/paid-action gates

Public, account, paid, deploy, publish, credential, destructive, GitHub, pull request, review-submission, issue-comment, merge, branch, commit, push, tag, release, GitHub Pages, or product-code actions are blocked. Human approval is required before any later commit, push, pull request, publication, deployment, account action, or other public GitHub action, and that approval must name the exact action and target.

## 6. Budgets and limits

- **Repository limit:** one explicitly assigned repository/worktree.
- **Write limit:** documentation files and one local repair report only.
- **Command limit:** local reads, scoped documentation generators/checks, and `git status`/`git diff`/`git log`.
- **Network limit:** zero network access; public documentation needed for repair context must be supplied inside the assigned repository/worktree by the human controller before repair.
- **Retry limit:** if a command may mutate product behavior or its scope is ambiguous, do not run it.
- **Evidence limit:** cite enough context to explain each documentation repair without copying private paths, credential-like strings, secret-like material, or excessive source text.

## 7. Stop conditions

Stop if the task needs product source/test/schema/script behavior changes, dependency or lockfile changes, CI/workflow changes outside Markdown comments, commit/push/pull request authority, public GitHub action, account action, credentials, private data outside scope, `.env` or credential-store reads, secret/key/token discovery, broad filesystem access, unclear repository assignment, ambiguity about whether a file is documentation or product code, ambiguous approval, deployment, publish authority, paid action, or a security-audit/compliance guarantee.

## 8. Human review point

Hermes/Jordan review is required before any product source/test/schema/script behavior change, dependency change, lockfile change, CI/workflow change outside Markdown comments, commit, branch, merge, push, pull request, review submission, issue comment, release, deploy, account action, public publish, GitHub Pages action, credential access, paid action, or expansion beyond one assigned repository/worktree. Any later approval for commit, push, pull request, or publication must name the exact action and target.

## 9. Audit-log fields

Record: `run_id`, `policy_card_path`, `assigned_repository`, `assigned_worktree`, `files`, `files_read`, `files_changed`, `documentation_paths_changed`, `commands_run`, `git_status`, `git_diff_summary`, `git_log_scope`, `verification`, `repair_report_path`, `residual_risks`, `blocked_actions`, `human_review_needed`, `next_safe_action`.

## 10. Governance category map

- **Policy:** pass - documentation-only repository repair, prohibited actions, and review gates are explicit.
- **Identity:** pass - worker lane and reviewer are named.
- **Sandbox:** pass - scope is limited to one assigned repository/worktree with documentation-only write authority.
- **Audit:** pass - files, commands, verification, repair report, residual risks, and blocked actions must be recorded.
- **Kill switch:** pass - stop conditions cover ambiguity, credentials, product-code mutation, public/account action, and publication.
- **Budget:** pass - repository, write, command, network, retry, and evidence limits are stated.
- **Provenance:** pass - documentation repairs must be tied to existing repository evidence.
- **Compliance evidence:** internal review evidence only; no certification, compliance review, security audit guarantee, runtime permission grant, or permission to ship.
