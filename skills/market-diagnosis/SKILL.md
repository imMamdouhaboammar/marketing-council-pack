---
name: market-diagnosis
description: Use when the user asks what is wrong with marketing performance, why growth stalled, where demand is constrained, or which marketing problem should be solved before choosing tactics.
license: MIT
metadata:
  version: "1.3.0"
---

# Market Diagnosis

**Goal:** Identify the smallest commercially meaningful bottleneck before prescribing activity.

## Process

1. Define the business outcome and time window.
2. Map the path from market availability to purchase, repeat purchase, and contribution.
3. Locate the dominant constraint: demand, awareness, comprehension, preference, access, price, trust, conversion, retention, capacity, or measurement.
4. Separate observed evidence from plausible causes.
5. Rank causes by expected impact, evidence strength, and reversibility.
6. Recommend the next decision or experiment, not a broad tactic list.

## Council roles

- `../../agents/market-architect.md`
- `../../agents/commercial-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Principles: `market-definition`, `customer-need-over-product`, `competitive-structure`
- Applied theories: `marketing-myopia`, `five-forces`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
