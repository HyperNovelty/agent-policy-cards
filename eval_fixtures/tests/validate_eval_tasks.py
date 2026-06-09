#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas' / 'eval_task.schema.json'
EXAMPLE = ROOT / 'examples' / 'eval_tasks.source_sufficiency_fixture.json'
TASK_RE = re.compile(r'^[a-z0-9][a-z0-9_\-]{2,140}$')
LANES = {'source_intake', 'citation_sufficiency', 'review_packet', 'education_adaptation', 'agent_handoff', 'operator_checklist'}


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    schema = load(SCHEMA)
    doc = load(EXAMPLE)
    require(schema.get('properties', {}).get('safety_mode', {}).get('const') == 'local_eval_fixture_only', 'schema safety const missing')
    require(doc.get('safety_mode') == 'local_eval_fixture_only', 'fixture safety invalid')
    tasks = doc.get('tasks')
    require(isinstance(tasks, list) and tasks, 'tasks must be non-empty')
    seen = set()
    for i, task in enumerate(tasks):
        pref = f'tasks[{i}]'
        for key in ['task_id', 'title', 'lane', 'user_goal', 'inputs', 'allowed_actions', 'blocked_actions', 'expected_artifacts', 'pass_criteria', 'failure_modes', 'review_gate']:
            require(key in task, f'{pref} missing {key}')
        require(TASK_RE.match(task['task_id']), f'{pref}.task_id invalid')
        require(task['task_id'] not in seen, f'duplicate task_id {task["task_id"]}')
        seen.add(task['task_id'])
        require(task['lane'] in LANES, f'{pref}.lane invalid')
        for key in ['inputs', 'allowed_actions', 'blocked_actions', 'expected_artifacts', 'pass_criteria', 'failure_modes']:
            require(isinstance(task[key], list) and all(isinstance(x, str) and x for x in task[key]), f'{pref}.{key} must be non-empty string array')
        blocked = ' '.join(task['blocked_actions']).lower()
        require('publish' in blocked and ('account' in blocked or 'credentials' in blocked or 'frameworks' in blocked), f'{pref}.blocked_actions lacks public/account gate')
        require('review' in task['review_gate'].lower() or 'approval' in task['review_gate'].lower(), f'{pref}.review_gate lacks human review/approval wording')
    print(f'schema={SCHEMA}')
    print(f'validated_eval_tasks={len(tasks)}')
    print('eval_task_validation=ok')
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f'eval_task_validation=failed error={exc}', file=sys.stderr)
        raise SystemExit(1)
