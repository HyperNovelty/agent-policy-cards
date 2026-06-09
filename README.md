# agent-policy-cards

Agent policy cards, eval fixtures, and verifiable research packet templates for bounded AI-agent workflows.



## Development

Run the validators with:

```bash
python3 validate_agent_policy_card.py --self-test
python3 check_policy_card_registry.py
python3 eval_fixtures/tests/validate_eval_tasks.py
python3 -m unittest discover -s tests
```

For machine-readable card validation output:

```bash
python3 validate_agent_policy_card.py --json examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md
python3 validate_agent_policy_card.py --json-out /tmp/policy-card-report.json examples/AGENT_POLICY_CARD_CODEX_LOCAL_PRODUCTIZATION_LANE_2026-06-07.md
```
