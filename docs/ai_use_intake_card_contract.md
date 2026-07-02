# AI Use Intake Card Contract

The AI Use Intake Card is a local, public-safe review aid for describing an AI-enabled workflow before deciding whether it needs a full policy card, authority envelope, stronger evidence, or human review.

It is not compliance approval, enforcement, certification, legal advice, deployment approval, or permission to operate a system.

## Required Contract

- `card_type` must be `ai_use_intake`.
- `status` must remain local-only, such as `sample_local_only` or `draft_local_only`.
- `decision_or_output` must describe what the AI produces and what it does not do.
- `human_review_required` must be explicit.
- `consequential_decision_exposure` must identify whether automation could affect people, accounts, eligibility, refunds, access, or similar outcomes.
- `next_gate` must route higher-risk uses to `policy_card`, `authority_envelope`, `human_review`, or `do_not_proceed`.
- `not_approval_statement` must say the card is not compliance approval, deployment approval, legal advice, or permission to operate.

## Safety Checks

The stdlib validator rejects checked-in cards that:

- include private local-user paths such as `/home/`, `file:///home/`, or `C:\Users\`;
- include obvious secret-like strings;
- claim the system sends messages, posts publicly, changes account settings, approves refunds or eligibility, or takes consequential action without explicit human review;
- route consequential or action-taking uses without a stricter next gate;
- present intake as deployment approval, compliance approval, certification, legal advice, or permission to operate.

## Local Validation

```bash
python3 tests/validate_ai_use_intake_card.py
```

Expected output includes a valid fixture passing and an invalid fixture being blocked.
