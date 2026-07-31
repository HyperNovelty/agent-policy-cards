# Roadmap

This repository is intended to be useful to maintainers building bounded AI-agent workflows, including Codex-assisted development, review, and documentation work.

## Near-term maintainer work

- Keep validators standard-library only so policy cards can be checked in CI without paid services.
- Expand negative fixtures for unsafe authority expansion, broad filesystem access, secret exposure, and unreviewed public/account actions.
- Add small example policy cards for common maintainer lanes: issue triage, documentation repair, test generation, and bounded security-review preparation.
- Keep generated reports advisory: no card should grant runtime authority by itself.

## Program fit

- **Codex for OSS:** Codex can help maintain issue triage, fixture expansion, validator hardening, and documentation repair for an active public repo.
- **Codex Open Source Fund:** API credits would support test-case generation and evaluation of agent-policy patterns without pushing costs into closed production work.

## Good first issues

- Add a negative fixture for accidental secret inclusion in policy-card examples.
- Add a sample policy card for issue triage.
- Improve README examples with before/after unsafe vs safe policy snippets.
- Add registry-level JSON aggregation for multi-command CI dashboards on top of the per-validator JSON export.
