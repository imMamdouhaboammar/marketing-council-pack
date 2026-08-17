---
name: pricing-strategy
description: Use when the user needs to set, change, package, test, defend, compare, or communicate price, discounts, plans, tiers, bundles, willingness-to-pay assumptions, or pricing economics.
---

# Pricing Strategy

**Goal:** Choose pricing decisions that reflect value, competition, economics, and buyer behavior.

## Process

1. Define the pricing decision: level, metric, package, discount, tier, or communication.
2. Calculate floor constraints from contribution economics.
3. Review alternatives and buyer reference points with current evidence when available.
4. Identify which customer differences justify packaging differences.
5. Model likely volume, margin, conversion, churn, or sales-cycle effects as ranges, not certainties.
6. Define a test or rollout rule with success and failure thresholds.

## Council roles

- `../../agents/commercial-strategist.md`
- `../../agents/positioning-strategist.md`
- `../../agents/behavior-strategist.md`

## Neural connections

- Principles: `commercial-reality`, `behavioral-framing`, `competitive-structure`
- Applied theories: `behavioral-framing`, `five-forces`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
