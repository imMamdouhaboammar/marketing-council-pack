#!/usr/bin/env python3
"""Simple two-proportion experiment planning helpers."""
from __future__ import annotations
import argparse
import json
import math
from statistics import NormalDist


def _prob(name: str, value: float, inclusive_zero: bool = True) -> float:
    value = float(value)
    low_ok = value >= 0 if inclusive_zero else value > 0
    if not low_ok or value >= 1:
        op = ">= 0" if inclusive_zero else "> 0"
        raise ValueError(f"{name} must be {op} and < 1")
    return value


def two_proportion_sample_size(
    baseline_rate: float,
    minimum_detectable_absolute_change: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> dict:
    p1 = _prob("baseline_rate", baseline_rate)
    delta = float(minimum_detectable_absolute_change)
    if delta <= 0:
        raise ValueError("minimum_detectable_absolute_change must be > 0")
    p2 = p1 + delta
    if p2 >= 1:
        raise ValueError("baseline_rate + minimum_detectable_absolute_change must be < 1")
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1")
    if not 0 < power < 1:
        raise ValueError("power must be between 0 and 1")

    z_alpha = NormalDist().inv_cdf(1 - alpha / 2)
    z_power = NormalDist().inv_cdf(power)
    pooled = (p1 + p2) / 2
    numerator = (
        z_alpha * math.sqrt(2 * pooled * (1 - pooled))
        + z_power * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
    ) ** 2
    n = math.ceil(numerator / (delta ** 2))
    return {
        "baseline_rate": p1,
        "target_rate": p2,
        "absolute_change": delta,
        "alpha": alpha,
        "power": power,
        "per_variant": n,
        "total": n * 2,
        "note": "Approximate equal-allocation two-sided two-proportion z-test planning estimate.",
    }


def summarize_uplift(control_rate: float, variant_rate: float) -> dict:
    control = _prob("control_rate", control_rate)
    variant = _prob("variant_rate", variant_rate)
    absolute = variant - control
    relative = (absolute / control) if control else None
    return {
        "control_rate": control,
        "variant_rate": variant,
        "absolute_change": absolute,
        "relative_uplift": relative,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Plan or summarize a two-proportion experiment.")
    sub = p.add_subparsers(dest="cmd", required=True)
    plan = sub.add_parser("plan")
    plan.add_argument("--baseline-rate", type=float, required=True)
    plan.add_argument("--mde", type=float, required=True)
    plan.add_argument("--alpha", type=float, default=0.05)
    plan.add_argument("--power", type=float, default=0.80)
    up = sub.add_parser("uplift")
    up.add_argument("--control-rate", type=float, required=True)
    up.add_argument("--variant-rate", type=float, required=True)
    args = p.parse_args()
    try:
        if args.cmd == "plan":
            result = two_proportion_sample_size(args.baseline_rate, args.mde, args.alpha, args.power)
        else:
            result = summarize_uplift(args.control_rate, args.variant_rate)
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
