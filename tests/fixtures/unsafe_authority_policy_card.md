# Agent Policy Card - Unsafe Authority Regression Fixture

## 1. Job identity
- **Job / worker name:** unsafe-fixture
- **Purpose:** exercise validator failures

## 2. Allowed scope
- `/`

## 3. Explicit exclusions
- credentials are blocked, but the card still hints that publish and account actions may be allowed after self-approval.

## 4. Evidence required before reporting success
- verification

## 5. Public/account/paid-action gates
The agent may grant itself runtime permission to publish after a local check.

## 6. Budgets and limits
- one run

## 7. Stop conditions
Stop on deploy only if the agent decides risk is too high.

## 8. Human review point
Review is optional.

## 9. Audit-log fields
`run_id`, `policy_card_path`, `files`, `verification`, `blocked_actions`, `next_safe_action`

## 10. Governance category map
Policy, identity, sandbox, audit, kill switch, budget, provenance, compliance evidence.
