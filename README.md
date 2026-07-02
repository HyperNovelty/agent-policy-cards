# agent-policy-cards

This is an early public candidate repo for drafting bounded agent-policy cards, validating them locally, and packaging report-only research artifacts. It is intentionally documentation-first: the cards and validators describe allowed scope and safety boundaries, but they do not grant runtime authority or enable external side effects by themselves.

## Why this exists

Agent workflows are easier to review when their purpose, allowed scope, exclusions,
evidence, stop conditions, and human review gates are written down before anyone
treats them as reusable. This repository keeps those cards local and static so
they can be inspected, tested, and improved without implying deployment,
credential access, account actions, or adoption.

## What this is

Use this repository to prototype narrow AI-agent lanes with explicit limits, local validation, and auditable examples. The current focus is safety-bounded maintainer workflows, synthetic/public-safe fixtures, and reusable templates that stay honest about maturity: useful for review and iteration now, not presented as a complete enforcement system.

The validator also includes negative fixtures for blocked cases such as cards
that ask agents to search for secrets/API keys or grant public posting and
account-setting authority without explicit approval gates.

## Examples

The examples directory shows several bounded workflow patterns you can inspect alongside the validators and registry:

- `CODEX_LOCAL_PRODUCTIZATION_LANE`: local productization/documentation lane with repo-only scope and review gates.
- `DAILY_AI_TOOL_SCOUT`: recurring scouting workflow framed as research/report output, not autonomous action.
- `IPUBLISHOS_DASHBOARD_EDITOR_PATCH`: bounded dashboard editing lane with explicit patch-review expectations.
- `SOURCE_TO_SYSTEM_PROMOTION_LANE`: promotion workflow that keeps source review and approval separate from execution authority.
- `AI_USE_INTAKE_CARD`: local intake fixture for describing an AI-enabled workflow before deciding whether policy cards, authority envelopes, stronger evidence, or human review are needed.

See [docs/EXAMPLE_GALLERY.md](docs/EXAMPLE_GALLERY.md) for what each example
demonstrates and what it does not authorize.

The AI Use Intake Card contract is documented in
[docs/ai_use_intake_card_contract.md](docs/ai_use_intake_card_contract.md).

## Repository policies

- [SECURITY.md](SECURITY.md): no-secrets and no-runtime-authority policy, plus
  responsible disclosure guidance.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md): compact participation and safety
  conduct note.

## Development

Run the validators with:

```bash
python3 validate_agent_policy_card.py --self-test
python3 check_policy_card_registry.py
python3 eval_fixtures/tests/validate_eval_tasks.py
python3 -m unittest discover -s tests
python3 tests/validate_ai_use_intake_card.py
```

For machine-readable card validation output:

```bash
python3 validate_agent_policy_card.py --json examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md
python3 validate_agent_policy_card.py --json-out /tmp/policy-card-report.json examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md
```
