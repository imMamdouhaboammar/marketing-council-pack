#!/usr/bin/env python3
"""Calculate stage and overall funnel conversion rates."""
from __future__ import annotations
import argparse
import json
from collections.abc import Mapping


def calculate_funnel(stages: Mapping[str, float]) -> dict:
    if len(stages) < 2:
        raise ValueError("at least two ordered funnel stages are required")
    items = [(str(k), float(v)) for k, v in stages.items()]
    for name, value in items:
        if value < 0:
            raise ValueError(f"stage {name} must be >= 0")
    rates: dict[str, float] = {}
    for (prev_name, prev), (name, value) in zip(items, items[1:]):
        if value > prev:
            raise ValueError(f"stage {name} cannot exceed prior stage {prev_name}")
        if prev == 0:
            rate = 0.0 if value == 0 else None
        else:
            rate = value / prev
        rates[f"{prev_name}_to_{name}"] = rate
    first = items[0][1]
    last = items[-1][1]
    overall = (last / first) if first else 0.0
    return {"stages": dict(items), "stage_rates": rates, "overall_conversion": overall}


def main() -> None:
    p = argparse.ArgumentParser(description="Calculate funnel conversion rates from ordered stage=count pairs.")
    p.add_argument("stage", nargs="+", help="Ordered items like visits=1000 leads=100 customers=20")
    args = p.parse_args()
    stages = {}
    try:
        for item in args.stage:
            name, raw = item.split("=", 1)
            stages[name] = float(raw)
        result = calculate_funnel(stages)
    except (ValueError, TypeError) as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
