#!/usr/bin/env python3
"""Rank marketing tactics with explicit weighted criteria."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

DEFAULT_WEIGHTS = {
    "impact": 0.18,
    "evidence": 0.15,
    "strategic_fit": 0.15,
    "audience_fit": 0.10,
    "channel_fit": 0.08,
    "measurement": 0.08,
    "speed": 0.05,
    "reversibility": 0.04,
    "cost": 0.06,
    "effort": 0.05,
    "risk": 0.06,
}
POSITIVE = {"impact", "evidence", "strategic_fit", "audience_fit", "channel_fit", "measurement", "speed", "reversibility"}
NEGATIVE = {"cost", "effort", "risk"}


def _validate_score(name: str, value: float) -> float:
    value = float(value)
    if not 0 <= value <= 10:
        raise ValueError(f"{name} must be between 0 and 10")
    return value


def rank_tactics(tactics: list[dict], weights: dict[str, float] | None = None) -> list[dict]:
    weights = dict(DEFAULT_WEIGHTS if weights is None else weights)
    required = POSITIVE | NEGATIVE
    if set(weights) != required:
        raise ValueError(f"weights must contain exactly: {', '.join(sorted(required))}")
    total_weight = sum(float(v) for v in weights.values())
    if total_weight <= 0:
        raise ValueError("weight total must be > 0")

    ranked = []
    for tactic in tactics:
        name = str(tactic.get("name", "")).strip()
        if not name:
            raise ValueError("each tactic requires a non-empty name")
        values = {k: _validate_score(k, tactic.get(k)) for k in required}
        weighted = 0.0
        for key in POSITIVE:
            weighted += (values[key] / 10) * float(weights[key])
        for key in NEGATIVE:
            weighted += ((10 - values[key]) / 10) * float(weights[key])
        score = 100 * weighted / total_weight
        ranked.append({**tactic, "score": round(score, 2)})
    return sorted(ranked, key=lambda x: (-x["score"], x["name"].lower()))


def main() -> None:
    p = argparse.ArgumentParser(description="Rank tactics from a JSON file containing a list of scored tactics.")
    p.add_argument("json_file", type=Path)
    args = p.parse_args()
    try:
        tactics = json.loads(args.json_file.read_text(encoding="utf-8"))
        result = rank_tactics(tactics)
    except (ValueError, OSError, json.JSONDecodeError, TypeError) as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
