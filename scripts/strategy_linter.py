#!/usr/bin/env python3
"""Lint strategy drafts for common Marketing Council failure modes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

GENERIC_PHRASES = (
    "build awareness",
    "engage the audience",
    "create valuable content",
    "use social media",
    "track kpis",
    "increase engagement",
)


def lint_strategy(text: str) -> list[dict]:
    lower = text.lower()
    findings: list[dict] = []
    hits = [p for p in GENERIC_PHRASES if p in lower]
    if hits:
        findings.append({
            "code": "generic-marketing-language",
            "severity": "warning",
            "message": "Generic marketing language found; define audience, mechanism, channel role, evidence, and measurement.",
            "matches": hits,
        })
    if not any(k in lower for k in ("what we will not do", "what we won't do", "exclusion", "deprioritize", "de-prioritize")):
        findings.append({
            "code": "missing-exclusion",
            "severity": "warning",
            "message": "No explicit strategic exclusion found. A strategy should state what is deliberately not being pursued.",
        })
    if "threshold" not in lower and "kill criterion" not in lower and "stop rule" not in lower:
        findings.append({
            "code": "missing-thresholds",
            "severity": "warning",
            "message": "No success/failure threshold or stop rule found.",
        })
    if "assumption" not in lower and "unknown" not in lower and "hypothesis" not in lower:
        findings.append({
            "code": "uncertainty-hidden",
            "severity": "info",
            "message": "No explicit assumptions, hypotheses, or unknowns found; verify that uncertainty is not being hidden.",
        })
    return findings


def main() -> None:
    p = argparse.ArgumentParser(description="Lint a Markdown marketing strategy draft.")
    p.add_argument("file", type=Path)
    args = p.parse_args()
    try:
        text = args.file.read_text(encoding="utf-8")
    except OSError as exc:
        p.error(str(exc))
    print(json.dumps(lint_strategy(text), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
