# Security Policy

This repository contains static Agent Policy Card examples, validators, templates,
and report-only fixtures. It does not grant runtime authority, connect accounts,
handle secrets, deploy services, or approve public/account/paid/destructive
actions.

## No Secrets

Do not submit secrets, tokens, API keys, private keys, cookies, session files,
credentials, account exports, payment data, or private personal records in issues,
pull requests, examples, fixtures, or policy cards.

Example cards and tests should use synthetic or public-safe data only.

## No Runtime Authority

Policy cards in this repository are advisory/static documentation. They are not:

- runtime permission grants
- job routers or cron gates
- account authorization
- credential access approval
- deployment approval
- approval for publishing, posting, emailing, uploading, purchasing, or changing
  external systems

Any real public, account, credential, paid, deployment, or destructive action
requires separate explicit human approval outside this repository.

## Reporting a Vulnerability

Please report suspected security issues privately to the project maintainer using
the repository owner's published security contact or issue-triage process.

Do not include secrets or private account material in the report. Include a short
description, affected files or commands, expected impact, and a minimal
reproduction using synthetic data when possible.
