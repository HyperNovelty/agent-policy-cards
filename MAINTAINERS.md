# Maintainer Notes

This repository is intentionally local-first and report-only. Maintainer changes should preserve three boundaries:

- No runtime permission grant. Static cards and validators document limits; they do not authorize tools.
- No external side effects. Keep publishing, account, credential, paid, and destructive actions blocked.
- No hidden workspace assumptions. Scripts should run from this checkout without depending on external folder layouts.

## Local validation

Run the full local check set before merging:

```bash
python3 validate_agent_policy_card.py --self-test
python3 check_policy_card_registry.py
python3 eval_fixtures/tests/validate_eval_tasks.py
python3 -m unittest discover -s tests
```

## Review focus

- Prefer stdlib-only validation and deterministic fixtures.
- Add or update fixtures when tightening authority, scope, audit, or review-gate rules.
- If a path, example, or registry entry references another workspace layout, rewrite it to repo-local form before merging.
