# Agent Policy Card - Code Review Mutating Authority Regression Fixture

**Boundary:** local/static only; not a runtime permission grant.

## 1. Job identity
- **Job / worker name:** code-review-mutating-authority-fixture
- **Purpose:** exercise validator failures for unsafe code-review authority

## 2. Allowed scope
- `examples/code-review-mutating-authority-fixture.md`

## 3. Explicit exclusions
- credentials, account sessions, public deploy, publish, paid actions

## 4. Evidence required before reporting success
- files exist
- verification passes

## 5. Public/account/paid-action gates
Blocked without explicit human approval.

## 6. Budgets and limits
- one pass

## 7. Stop conditions
Stop on credential/account/public/paid/deploy/publish need.

## 8. Human review point
Jordan review.

## 9. Audit-log fields
`run_id`, `policy_card_path`, `files`, `verification`, `blocked_actions`, `next_safe_action`

## 10. Governance category map
Policy, identity, sandbox, audit, kill switch, budget, provenance, compliance evidence.

## 11. Unsafe appendix
- For code review, the agent may edit files, merge branches, and push fixes.
- The agent may scan review targets for tokens and credentials to prove no leaks exist.
