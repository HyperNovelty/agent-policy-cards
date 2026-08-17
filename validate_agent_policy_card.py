#!/usr/bin/env python3
"""Static validator for Agent Policy Cards.

Local-only / advisory. This script reads Markdown policy cards and checks for
required sections, explicit blocked-action language, evidence/audit fields, and
high-level governance categories. It does not execute card contents and does not
grant runtime authority.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent

REQUIRED_HEADINGS = [
    "job identity",
    "allowed scope",
    "explicit exclusions",
    "evidence required before reporting success",
    "public/account/paid-action gates",
    "budgets and limits",
    "stop conditions",
    "human review point",
    "audit-log fields",
    "governance category map",
]

REQUIRED_BLOCKED_TERMS = [
    "credential",
    "public",
    "account",
    "paid",
    "deploy",
    "publish",
]

REQUIRED_AUDIT_FIELDS = [
    "run_id",
    "policy_card_path",
    "files",
    "verification",
    "blocked_actions",
    "next_safe_action",
]

REQUIRED_CATEGORIES = [
    "policy",
    "identity",
    "sandbox",
    "audit",
    "kill switch",
    "budget",
    "provenance",
    "compliance evidence",
]

PLACEHOLDER_MARKERS = ["<short stable name>", "<what useful outcome", "<exact local", "<approved source", "<exact destination", "<search/read", "<e.g."]

UNSAFE_AUTHORITY_PATTERNS = [
    r"grant itself runtime permission",
    r"self-approval",
    r"self approval",
    r"review is optional",
]

SECRET_LIKE_PATTERNS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\bAKIA[0-9A-Z]{16}\b",
    r"\bghp_[A-Za-z0-9]{20,}\b",
    r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b",
]

UNSAFE_SECRET_SEARCH_PATTERNS = [
    r"\b(search|scan|grep|find|look for)\b.{0,80}\b(api keys?|secrets?|tokens?|credentials?)\b",
]

UNSAFE_UNGATED_PUBLIC_ACCOUNT_PATTERNS = [
    r"\b(publish|post|upload|share|change account settings|edit account settings)\b.{0,120}\b(without|no)\b.{0,40}\b(explicit )?(human )?(approval|review)\b",
]

CODE_REVIEW_CONTEXT_RE = re.compile(r"\b(?:during|for)\s+(?:code\s+)?review\b|\bcode\s+review\b")
CODE_REVIEW_ACTOR_RE = re.compile(
    r"\b(?:code\s+review(?:er|ers| agents?| lane| worker)|review\s+agent)\b"
)
OTHER_ACTOR_RE = re.compile(r"\b(?:implementation|implementer|patch|editing)\s+agent\b")
REVIEW_PASSIVE_RECIPIENT_RE = re.compile(
    r"\b(?:by|for|to)\s+(?:the\s+|a\s+|an\s+)?"
    r"(?:code\s+review(?:er|ers| agents?)|review\s+agent)\b"
)
OTHER_PASSIVE_RECIPIENT_RE = re.compile(
    r"\b(?:by|for|to)\s+(?:the\s+|a\s+|an\s+|separate\s+)?"
    r"(?:implementation|implementer|patch|editing)\s+agents?\b"
)
ISSUE_TRIAGE_CONTEXT_RE = re.compile(
    r"\b(?:issue[-\s]?triage|triage\s+(?:agents?|lanes?|workers?|report|recommendation)|"
    r"repository\s+issue|issue\s+packet)\b"
)
ISSUE_TRIAGE_ACTOR_RE = re.compile(
    r"\b(?:issue[-\s]?triage\s+(?:agents?|lanes?|workers?)|triage\s+(?:agents?|lanes?|workers?))\b"
)
OTHER_ISSUE_TRIAGE_ACTOR_RE = re.compile(
    r"\b(?:separate\s+)?(?:implementation|implementer|patch|editing)\s+agents?\b|"
    r"\b(?:human\s+)?maintainers?\b|"
    r"\bhuman\s+(?:reviewers?|operators?)\b"
)
ISSUE_TRIAGE_PASSIVE_OTHER_RECIPIENT_RE = re.compile(
    r"\b(?:by|for|to)\s+(?:the\s+|a\s+|an\s+|separate\s+)?"
    r"(?:(?:implementation|implementer|patch|editing)\s+agents?|"
    r"(?:human\s+)?maintainers?|human\s+(?:reviewers?|operators?))\b"
)
GENERIC_AGENT_RE = re.compile(
    r"\b(?:the\s+|an?\s+)?agents?\b"
)
ISSUE_TRIAGE_MUTATION_ACTION_RE = re.compile(
    r"\b(?:(?:add|remove|apply|change|set)\s+labels?|comment|comments|commenting|"
    r"label|labeling|assign|assigns|assigning|set\s+milestones?|milestoning|"
    r"close|closes|closing|closed|reopen|reopens|"
    r"reopening|state\s+change|state\s+changes|change\s+state|changes\s+state|"
    r"open\s+(?:a\s+)?(?:pr|pull\s+request)|create\s+(?:a\s+)?(?:pr|pull\s+request)|"
    r"patch|patches|patching|commit|commits|committing|push|pushes|pushing)\b"
)
ISSUE_TRIAGE_PASSIVE_MUTATION_GRANT_RE = re.compile(
    r"\b(?:comments?|labels?|assignments?|milestones?|state\s+changes?|closure|reopening|"
    r"pull\s+requests?|prs?|patches|commits?|pushes)\b.{0,50}\b(?:is|are)\s+"
    r"(?:allowed|permitted|authorized)\b"
)
ISSUE_TRIAGE_PROMOTION_PATTERNS = [
    r"\b(?:triage\s+)?recommendation\b.{0,80}\b(?:is|counts\s+as|becomes)\b.{0,40}\b"
    r"(?:a\s+)?(?:maintainer\s+)?(?:decision|assignment|acceptance|priority|schedule)\b",
    r"\b(?:triage\s+)?report\b.{0,80}\b(?:decides|assigns|accepts|prioritizes|schedules|closes)\b",
    r"\b(?:issue[-\s]?triage|triage\s+(?:agent|lane|worker))\b.{0,100}\b"
    r"(?:decides|assigns|accepts|prioritizes|schedules|closes)\b",
]
ISSUE_TRIAGE_PROMOTION_TARGET_RE = re.compile(
    r"\b(?:decision|assignment|acceptance|priority|schedule|assigned|accepted|prioritized|closed|"
    r"decides|assigns|accepts|prioritizes|schedules|closes)\b"
)
ISSUE_TRIAGE_SOURCE_FACT_PASSIVE_RE = re.compile(
    r"\b(?:already\s+present|existing|pre[-\s]?existing|supplied|provided|recorded|current|"
    r"historical|previously\s+(?:applied|recorded|set|assigned)|from\s+the\s+(?:supplied\s+)?"
    r"(?:issue\s+)?packet|on\s+the\s+(?:supplied\s+)?(?:repository\s+)?issue)\b"
    r".{0,80}\b(?:as|for)\s+(?:source\s+facts?|source\s+evidence|evidence|input\s+facts?)\b"
)
NEGATED_REVIEW_RECIPIENT_RE = re.compile(
    r"\bnot\s+(?:the\s+|a\s+|an\s+)?(?:code\s+review(?:er|ers| agents?)|review\s+agent)\b"
)
GENERIC_REVIEW_AGENT_RE = re.compile(r"\b(?:the\s+)?agent\b")
PRONOUN_ACTOR_RE = re.compile(r"\bit\b")
MUTATION_AUTHORITY_RE = re.compile(
    r"\b(?:may|can|(?:is|are|be|being)\s+(?:allowed|permitted|authorized)\s+to|"
    r"(?:allowed|permitted|authorized)\s+to|ha(?:s|ve)\s+permission\s+to)\b"
)
MUTATION_ACTION_CANDIDATE_RE = re.compile(
    r"\b(edit|edits|editing|patch|patches|patching|format|formats|formatting|"
    r"commit|commits|committing|branch|branches|branching|merge|merges|merging|"
    r"push|pushes|pushing|submit|submits|submitting|modify|modifies|modifying|"
    r"update|updates|updating|rewrite|rewrites|rewriting|delete|deletes|deleting|"
    r"create|creates|creating|write|writes|writing|apply|applies|applying)\b"
)
PASSIVE_MUTATION_GRANT_RE = re.compile(
    r"\b(?:editing|edits|file\s+edits|code\s+changes|patching|modifying|updating|"
    r"rewriting|deleting|creating|formatting)\b.{0,40}\b(?:is|are)\s+"
    r"(?:allowed|permitted|authorized)\b"
)
MUTATION_PAIR_MAX_CHARS = 100
MUTATION_CONTEXT_MAX_CHARS = 180


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def normalize_mutation_authority_text(text: str) -> str:
    lowered = text.lower()
    without_hyphenation = re.sub(r"(?<=\w)-(?=\w)", " ", lowered)
    return "\n".join(re.sub(r"[ \t\r\f\v]+", " ", line).strip() for line in without_hyphenation.splitlines())


def sentence_like_segments(text: str) -> list[str]:
    segments: list[str] = []
    pending = ""
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            pending = ""
            continue
        if pending:
            stripped = f"{pending} {stripped}"
            pending = ""
        if stripped.endswith(",") and not re.match(r"^\s*[-*+]\s+", line):
            pending = stripped
            continue
        segments.extend(segment.strip() for segment in re.split(r"[.!?]+", stripped) if segment.strip())
    if pending:
        segments.append(pending.strip())
    return segments


def last_clause_start(segment: str, position: int) -> int:
    starts = [segment.rfind(mark, 0, position) for mark in (";", ",")]
    return max(starts) + 1


def next_authority_start(segment: str, authority: re.Match[str]) -> int:
    next_authority = MUTATION_AUTHORITY_RE.search(segment, authority.end())
    return next_authority.start() if next_authority else len(segment)


def clause_bounds(segment: str, start: int, end: int) -> tuple[int, int]:
    clause_start = last_clause_start(segment, start)
    clause_end = len(segment)
    for mark in (";", ","):
        position = segment.find(mark, end)
        if position != -1:
            clause_end = min(clause_end, position)
    return clause_start, clause_end


def has_review_actor_for_authority(segment: str, authority: re.Match[str], previous_review_clause: bool) -> bool:
    clause_start = last_clause_start(segment, authority.start())
    local_prefix = segment[clause_start : authority.start()]
    sentence_has_review_context = bool(CODE_REVIEW_CONTEXT_RE.search(segment))

    if OTHER_ACTOR_RE.search(local_prefix):
        return False
    if CODE_REVIEW_ACTOR_RE.search(local_prefix):
        return True
    if GENERIC_REVIEW_AGENT_RE.search(local_prefix) and sentence_has_review_context:
        return True
    if PRONOUN_ACTOR_RE.search(local_prefix) and previous_review_clause:
        return True
    if previous_review_clause and re.fullmatch(r"\s*(?:and|but|also|then)?\s*", local_prefix):
        return True
    if CODE_REVIEW_CONTEXT_RE.search(local_prefix) and GENERIC_REVIEW_AGENT_RE.search(segment[authority.start() : authority.end() + 25]):
        return True
    return False


def passive_mutation_grant_is_review_authority(segment: str, grant: re.Match[str]) -> bool:
    clause_start, clause_end = clause_bounds(segment, grant.start(), grant.end())
    clause = segment[clause_start:clause_end]
    grant_text = segment[grant.start() : grant.end()]

    if REVIEW_PASSIVE_RECIPIENT_RE.search(clause):
        return True
    if OTHER_PASSIVE_RECIPIENT_RE.search(clause) or NEGATED_REVIEW_RECIPIENT_RE.search(clause):
        return False
    if CODE_REVIEW_ACTOR_RE.search(grant_text):
        return True
    return bool(CODE_REVIEW_CONTEXT_RE.search(segment))


def mutation_candidate_is_mutating(segment: str, mutation: re.Match[str]) -> bool:
    verb = mutation.group(1)
    tail = segment[mutation.end() : mutation.end() + 60]

    if verb in {"write", "writes", "writing"}:
        return bool(
            re.match(
                r"\s+(?:a\s+|an\s+|the\s+)?(?:files?|code|fix(?:es)?|changes?|patch(?:es)?|diffs?)\b",
                tail,
            )
        )
    if verb in {"apply", "applies", "applying"}:
        return bool(re.match(r"\s+(?:a\s+|an\s+|the\s+)?(?:fix(?:es)?|changes?|patch(?:es)?)\b", tail))
    if verb in {"submit", "submits", "submitting"}:
        return bool(re.match(r"\s+(?:review\s+)?(?:changes?|fix(?:es)?|patch(?:es)?)\b", tail))
    return True


def denied_mutation_pair(segment: str, authority: re.Match[str], mutation: re.Match[str]) -> bool:
    before_authority = segment[max(0, authority.start() - 40) : authority.start()]
    authority_to_mutation = segment[authority.start() : mutation.start()]
    through_mutation = segment[authority.start() : mutation.end()]

    if re.search(r"\bnot\s+(?:only|just)\b", authority_to_mutation):
        return False
    if re.search(r"\b(?:not|never|cannot|can\s+not|may\s+not|may\s+never)\b", authority_to_mutation):
        return True
    if re.search(r"\b(?:not|never|cannot|can\s+not|may\s+not|may\s+never)\b\s*$", before_authority):
        return True
    if re.search(r"\bnot\s+(?:allowed|permitted|authorized)\s+to\b", before_authority + through_mutation):
        return True
    if re.search(
        r"\bonly\s+(?:inspect|read)\b.{0,80}\bnot\b.{0,30}" + MUTATION_ACTION_CANDIDATE_RE.pattern,
        through_mutation,
    ):
        return True
    return False


def code_review_mutation_authority_evidence(text: str) -> list[str]:
    evidence: list[str] = []
    for segment in sentence_like_segments(normalize_mutation_authority_text(text)):
        contexts = list(CODE_REVIEW_CONTEXT_RE.finditer(segment)) + list(CODE_REVIEW_ACTOR_RE.finditer(segment))
        passive_grants = list(PASSIVE_MUTATION_GRANT_RE.finditer(segment))
        if contexts:
            blocked_passive_grants = [
                grant for grant in passive_grants if passive_mutation_grant_is_review_authority(segment, grant)
            ]
            if blocked_passive_grants:
                evidence.append(segment.strip())
                continue

        authorities = list(MUTATION_AUTHORITY_RE.finditer(segment))
        mutations = [match for match in MUTATION_ACTION_CANDIDATE_RE.finditer(segment) if mutation_candidate_is_mutating(segment, match)]
        previous_review_clause = False
        for authority in authorities:
            is_review_actor = has_review_actor_for_authority(segment, authority, previous_review_clause)
            clause_end = min(
                [pos for pos in (segment.find(";", authority.end()), next_authority_start(segment, authority)) if pos != -1]
                or [len(segment)]
            )
            if is_review_actor:
                previous_review_clause = True
            if not contexts or not is_review_actor:
                continue
            for mutation in mutations:
                if mutation.start() < authority.end():
                    continue
                if mutation.start() >= clause_end:
                    continue
                if mutation.start() - authority.end() > MUTATION_PAIR_MAX_CHARS:
                    continue
                if denied_mutation_pair(segment, authority, mutation):
                    continue

                pair_start = authority.start()
                pair_end = mutation.end()
                if not any(
                    abs(context.start() - pair_end) <= MUTATION_CONTEXT_MAX_CHARS
                    or abs(pair_start - context.end()) <= MUTATION_CONTEXT_MAX_CHARS
                    or (context.start() <= pair_start and pair_end <= context.end())
                    for context in contexts
                ):
                    continue

                evidence_start = max(0, min(pair_start, *(context.start() for context in contexts)) - 40)
                evidence_end = min(len(segment), max(pair_end, *(context.end() for context in contexts)) + 40)
                evidence.append(segment[evidence_start:evidence_end].strip())
                break
            else:
                continue
            break
    return evidence


def denied_issue_triage_authority(segment: str, authority: re.Match[str], mutation: re.Match[str]) -> bool:
    before_authority = segment[max(0, authority.start() - 45) : authority.start()]
    authority_to_mutation = segment[authority.start() : mutation.start()]
    through_mutation = segment[authority.start() : mutation.end()]

    if re.search(r"\bnot\s+(?:only|just)\b", authority_to_mutation):
        return False
    if re.search(r"\b(?:not|never|cannot|can\s+not|may\s+not|may\s+never|must\s+not)\b", authority_to_mutation):
        return True
    if re.search(r"\b(?:not|never|cannot|can\s+not|may\s+not|may\s+never|must\s+not)\b\s*$", before_authority):
        return True
    if re.search(r"\bnot\s+(?:allowed|permitted|authorized)\s+to\b", before_authority + through_mutation):
        return True
    return False


def has_issue_triage_actor_for_authority(segment: str, authority: re.Match[str], previous_triage_clause: bool) -> bool:
    clause_start = last_clause_start(segment, authority.start())
    local_prefix = segment[clause_start : authority.start()]
    sentence_has_triage_context = bool(ISSUE_TRIAGE_CONTEXT_RE.search(segment))

    if OTHER_ISSUE_TRIAGE_ACTOR_RE.search(local_prefix):
        return False
    if ISSUE_TRIAGE_ACTOR_RE.search(local_prefix):
        return True
    if GENERIC_AGENT_RE.search(local_prefix) and sentence_has_triage_context:
        return True
    if PRONOUN_ACTOR_RE.search(local_prefix) and previous_triage_clause:
        return True
    if previous_triage_clause and re.fullmatch(r"\s*(?:and|but|also|then)?\s*", local_prefix):
        return True
    return False


def passive_mutation_grant_is_issue_triage_authority(segment: str, grant: re.Match[str]) -> bool:
    clause_start, clause_end = clause_bounds(segment, grant.start(), grant.end())
    clause = segment[clause_start:clause_end]
    grant_text = segment[grant.start() : grant.end()]

    if ISSUE_TRIAGE_SOURCE_FACT_PASSIVE_RE.search(clause):
        return False
    if ISSUE_TRIAGE_PASSIVE_OTHER_RECIPIENT_RE.search(clause):
        return False
    if ISSUE_TRIAGE_ACTOR_RE.search(clause) or ISSUE_TRIAGE_ACTOR_RE.search(grant_text):
        return True
    return bool(ISSUE_TRIAGE_CONTEXT_RE.search(segment))


def issue_triage_mutation_authority_evidence(text: str) -> list[str]:
    evidence: list[str] = []
    for segment in sentence_like_segments(normalize_mutation_authority_text(text)):
        contexts = list(ISSUE_TRIAGE_CONTEXT_RE.finditer(segment))
        if not contexts:
            continue

        passive_grants = list(ISSUE_TRIAGE_PASSIVE_MUTATION_GRANT_RE.finditer(segment))
        if any(passive_mutation_grant_is_issue_triage_authority(segment, grant) for grant in passive_grants):
            evidence.append(segment.strip())
            continue

        authorities = list(MUTATION_AUTHORITY_RE.finditer(segment))
        mutations = list(ISSUE_TRIAGE_MUTATION_ACTION_RE.finditer(segment))
        previous_triage_clause = False
        for authority in authorities:
            is_triage_actor = has_issue_triage_actor_for_authority(segment, authority, previous_triage_clause)
            if is_triage_actor:
                previous_triage_clause = True
            if is_triage_actor:
                clause_end = min(
                    [pos for pos in (segment.find(";", authority.end()), next_authority_start(segment, authority)) if pos != -1]
                    or [len(segment)]
                )
                for mutation in mutations:
                    if mutation.start() < authority.end() or mutation.start() >= clause_end:
                        continue
                    if mutation.start() - authority.end() > MUTATION_PAIR_MAX_CHARS:
                        continue
                    if denied_issue_triage_authority(segment, authority, mutation):
                        continue
                    evidence.append(segment.strip())
                    break
            if evidence and evidence[-1] == segment.strip():
                break
    return evidence


def issue_triage_promotion_evidence(text: str) -> list[str]:
    evidence: list[str] = []
    for segment in sentence_like_segments(normalize_mutation_authority_text(text)):
        if not ISSUE_TRIAGE_CONTEXT_RE.search(segment):
            continue
        for pattern in ISSUE_TRIAGE_PROMOTION_PATTERNS:
            match = re.search(pattern, segment)
            if match and not issue_triage_promotion_match_is_negated(segment, match):
                evidence.append(segment.strip())
                break
    return evidence


def issue_triage_promotion_match_is_negated(segment: str, match: re.Match[str]) -> bool:
    targets = list(ISSUE_TRIAGE_PROMOTION_TARGET_RE.finditer(match.group(0)))
    if not targets:
        return False

    target = targets[-1]
    target_start = match.start() + target.start()
    target_end = match.start() + target.end()
    clause_start, _ = clause_bounds(segment, target_start, target_end)
    same_clause_prefix = segment[clause_start:target_start]
    return bool(
        re.search(
            r"\b(?:not|never|cannot|can\s+not|may\s+not|must\s+not|no)\b",
            same_clause_prefix,
        )
    )


def heading_texts(text: str) -> list[str]:
    out: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,4}\s+(.*)$", line.strip())
        if match:
            title = re.sub(r"^\d+\.\s*", "", match.group(1).strip().lower())
            out.append(title)
    return out


def path_mentions(text: str) -> list[str]:
    mentions: list[str] = []
    # Markdown/code-ish local paths only; URLs are intentionally ignored.
    for raw in re.findall(r"`([^`]+)`", text):
        if "/" in raw or raw.startswith("C:\\"):
            mentions.append(raw)
    return mentions


def is_broad_root(raw: str) -> bool:
    clean = raw.strip()
    broad = {"/", "~", "/home", "/home/aware1", "/home/aware1/.hermes", "/mnt/c", "C:\\", "C:\\Users", "C:\\Users\\Aware1"}
    if clean in broad:
        return True
    if ".." in Path(clean.replace("C:\\", "/mnt/c/")).parts:
        return True
    return False


def validate_text(text: str, *, allow_template_placeholders: bool = False) -> list[str]:
    failures: list[str] = []
    norm = normalize(text)
    headings = heading_texts(text)

    for required in REQUIRED_HEADINGS:
        if not any(required in h for h in headings):
            failures.append(f"missing required heading: {required}")

    for term in REQUIRED_BLOCKED_TERMS:
        if term not in norm:
            failures.append(f"missing blocked-action/gate term: {term}")

    for field in REQUIRED_AUDIT_FIELDS:
        if field not in norm:
            failures.append(f"missing audit/evidence field marker: {field}")

    for category in REQUIRED_CATEGORIES:
        if category not in norm:
            failures.append(f"missing governance category: {category}")

    if "runtime permission grant" not in norm and "not a runtime" not in norm:
        failures.append("missing explicit no-runtime-grant boundary")

    if "human approval" not in norm and "human review" not in norm and "jordan" not in norm:
        failures.append("missing human approval/review language")

    if not allow_template_placeholders:
        for marker in PLACEHOLDER_MARKERS:
            if marker.lower() in text.lower():
                failures.append(f"unfilled template placeholder remains: {marker}")

    for mention in path_mentions(text):
        if is_broad_root(mention):
            failures.append(f"path mention is too broad/unsafe: {mention}")

    for pattern in UNSAFE_AUTHORITY_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"unsafe authority expansion language detected: {pattern}")

    for pattern in SECRET_LIKE_PATTERNS:
        if re.search(pattern, text):
            failures.append(f"secret-like material detected: {pattern}")

    for pattern in UNSAFE_SECRET_SEARCH_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"unsafe secret-search authority detected: {pattern}")

    for pattern in UNSAFE_UNGATED_PUBLIC_ACCOUNT_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            failures.append(f"ungated public/account authority detected: {pattern}")

    for evidence in code_review_mutation_authority_evidence(text):
        failures.append(f"unsafe code-review mutation authority detected: {evidence}")

    for evidence in issue_triage_mutation_authority_evidence(text):
        failures.append(f"unsafe issue-triage mutation authority detected: {evidence}")

    for evidence in issue_triage_promotion_evidence(text):
        failures.append(f"unsafe issue-triage recommendation promotion detected: {evidence}")

    return failures


def validate_file(path: Path, *, allow_template_placeholders: bool = False) -> tuple[bool, list[str]]:
    text = path.read_text(encoding="utf-8")
    failures = validate_text(text, allow_template_placeholders=allow_template_placeholders)
    return not failures, failures


def build_report(paths: list[str], *, allow_template_placeholders: bool = False) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    summary = {"passed": 0, "failed": 0, "missing": 0, "total": 0}

    for raw in paths:
        path = Path(raw)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        rel = str(path.relative_to(PROJECT_ROOT)) if str(path).startswith(str(PROJECT_ROOT)) else str(path)
        entry: dict[str, Any] = {
            "input_path": raw,
            "path": rel,
            "exists": path.exists(),
            "ok": False,
            "failures": [],
        }
        summary["total"] += 1
        if not path.exists():
            entry["failures"] = ["file not found"]
            summary["missing"] += 1
            summary["failed"] += 1
            results.append(entry)
            continue

        ok, failures = validate_file(path, allow_template_placeholders=allow_template_placeholders)
        entry["ok"] = ok
        entry["failures"] = failures
        if ok:
            summary["passed"] += 1
        else:
            summary["failed"] += 1
        results.append(entry)

    return {
        "report_version": 1,
        "project_root": str(PROJECT_ROOT),
        "allow_template_placeholders": allow_template_placeholders,
        "summary": summary,
        "results": results,
    }


def print_text_report(report: dict[str, Any]) -> None:
    for item in report["results"]:
        if item["ok"]:
            print(f"PASS {item['path']}")
        else:
            print(f"FAIL {item['path']}")
            for failure in item["failures"]:
                print(f"  - {failure}")


def run_self_test() -> int:
    good = """# Agent Policy Card — Toy

**Boundary:** local/static only; not a runtime permission grant.

## 1. Job identity
- **Job / worker name:** toy
- **Purpose:** local test

## 2. Allowed scope
- `products/agent_os_authority_layer/examples/toy.md`

## 3. Explicit exclusions
- credentials, account sessions, public deploy, publish, paid actions

## 4. Evidence required before reporting success
- files exist
- verification passes

## 5. Public/account/paid-action gates
Blocked without explicit human approval.

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
"""
    bad = "# Agent Policy Card — Bad\n\nDo stuff.\n"
    with TemporaryDirectory() as tmp:
        good_path = Path(tmp) / "good.md"
        bad_path = Path(tmp) / "bad.md"
        good_path.write_text(good, encoding="utf-8")
        bad_path.write_text(bad, encoding="utf-8")
        good_ok, good_failures = validate_file(good_path)
        bad_ok, bad_failures = validate_file(bad_path)
    if not good_ok:
        print("SELF_TEST_FAIL: good fixture failed")
        for failure in good_failures:
            print(" -", failure)
        return 1
    if bad_ok:
        print("SELF_TEST_FAIL: bad fixture passed unexpectedly")
        return 1
    print("SELF_TEST_PASS")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate static Agent Policy Card Markdown files.")
    parser.add_argument("paths", nargs="*", help="Markdown card paths to validate")
    parser.add_argument("--self-test", action="store_true", help="run built-in validator self-test")
    parser.add_argument("--allow-template-placeholders", action="store_true", help="allow template placeholder markers")
    parser.add_argument("--json", action="store_true", help="emit a deterministic JSON validation report")
    parser.add_argument("--json-out", help="write the JSON validation report to a file")
    args = parser.parse_args(argv)

    if args.self_test:
        return run_self_test()
    if not args.paths:
        parser.error("provide at least one path or --self-test")

    report = build_report(args.paths, allow_template_placeholders=args.allow_template_placeholders)
    if args.json or args.json_out:
        payload = json.dumps(report, indent=2, sort_keys=True)
        if args.json_out:
            out_path = Path(args.json_out)
            if not out_path.is_absolute():
                out_path = PROJECT_ROOT / out_path
            out_path.write_text(payload + "\n", encoding="utf-8")
        if args.json:
            print(payload)
    else:
        print_text_report(report)
    return 1 if report["summary"]["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
