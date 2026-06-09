# Agent OS Local Eval Task Fixture Contract

Generated: 2026-06-06T23:07:02Z

## Purpose

This contract turns the Signals/Tools research into local eval tasks for iPublishOS and Agent OS. The eval is not a benchmark claim; it is a checkable workflow fixture.

Each task specifies:

- user goal,
- local inputs,
- allowed actions,
- blocked actions,
- expected artifacts,
- pass criteria,
- failure modes, and
- human review gate.

## Why this was the next recommended action

The June 6 packet recommended moving from raw source intake into source cards and eval schemas. This file is the eval-schema half of that move. It makes agent behavior testable before any broader automation or public surface is touched.

## Safety boundary

Local fixture only. No third-party installs, repo execution, browser/account connection, outreach, posting, publishing, DNS, payments, KYC, credentials, or public deployment.

## Verification

```bash
python3 products/agent_os_authority_layer/eval_fixtures/tests/validate_eval_tasks.py
```
