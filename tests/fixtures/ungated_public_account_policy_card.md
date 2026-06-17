# Agent Policy Card - Ungated Public Account Regression Fixture

**Boundary:** local/static only; not a runtime permission grant.

## 1. Job identity
- **Job / worker name:** ungated-public-account-fixture
- **Purpose:** exercise validator failures for public/account authority without approval gates

## 2. Allowed scope
- `examples/ungated-public-account-fixture.md`

## 3. Explicit exclusions
- credentials, account sessions, public deploy, publish, paid actions

## 4. Evidence required before reporting success
- files exist
- verification passes

## 5. Public/account/paid-action gates
Blocked without explicit human approval for paid deploy actions.

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
- The agent may publish public posts and change account settings without explicit human approval.
