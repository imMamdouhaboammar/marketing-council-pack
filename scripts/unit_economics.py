#!/usr/bin/env python3
"""Deterministic unit-economics calculations for marketing decisions."""
from __future__ import annotations
import argparse
import json


def _nonnegative(name: str, value: float) -> float:
    value = float(value)
    if value < 0:
        raise ValueError(f"{name} must be >= 0")
    return value


def calculate_unit_economics(
    revenue_per_order: float,
    cogs_per_order: float,
    variable_costs_per_order: float,
    cac: float,
    expected_orders_per_customer: float = 1.0,
) -> dict:
    revenue = _nonnegative("revenue_per_order", revenue_per_order)
    cogs = _nonnegative("cogs_per_order", cogs_per_order)
    variable = _nonnegative("variable_costs_per_order", variable_costs_per_order)
    acquisition = _nonnegative("cac", cac)
    orders = float(expected_orders_per_customer)
    if orders <= 0:
        raise ValueError("expected_orders_per_customer must be > 0")

    contribution = revenue - cogs - variable
    customer_contribution = contribution * orders
    net_customer_contribution = customer_contribution - acquisition
    contribution_margin_ratio = (contribution / revenue) if revenue else None
    break_even_roas = (revenue / contribution) if contribution > 0 else None

    return {
        "revenue_per_order": revenue,
        "contribution_per_order": contribution,
        "contribution_margin_ratio": contribution_margin_ratio,
        "expected_orders_per_customer": orders,
        "customer_contribution_before_acquisition": customer_contribution,
        "cac": acquisition,
        "net_customer_contribution": net_customer_contribution,
        "max_break_even_cac": customer_contribution,
        "break_even_roas": break_even_roas,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Calculate simple unit economics.")
    p.add_argument("--revenue-per-order", type=float, required=True)
    p.add_argument("--cogs-per-order", type=float, required=True)
    p.add_argument("--variable-costs-per-order", type=float, default=0)
    p.add_argument("--cac", type=float, default=0)
    p.add_argument("--expected-orders-per-customer", type=float, default=1)
    args = p.parse_args()
    try:
        result = calculate_unit_economics(**vars(args))
    except ValueError as exc:
        p.error(str(exc))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
