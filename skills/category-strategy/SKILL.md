---
name: category-strategy
description: Use when the user needs category definition, category creation, category entry logic, market framing, competitive context, or a decision about which market the offer should compete in.
---

# Category Strategy

**Goal:** Choose a category frame that helps buyers understand the offer and gives the company a credible competitive field.

## Process

1. Name the decision and the evidence available.
2. Activate only theories that explain the observed constraint.
3. Compare at least one credible counterweight when the choice is strategic.
4. Produce one primary recommendation with mechanism, trade-off, and measurement.
5. State what evidence would reverse the recommendation.

## Council roles

- `../../agents/market-architect.md`
- `../../agents/positioning-strategist.md`
- `../../agents/competitive-strategy-analyst.md`

## Neural connections

- Applied theories: `marketing-myopia`, `positioning-components`, `five-forces`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Challenge with `../../hooks/theory-fit-gate.md` and `../../hooks/causal-mechanism-check.md` when theory choice or causality is load-bearing.

## Required output

Return the decision, supporting evidence, assumptions, selected theory or mechanism, rejected alternative, measurement, confidence, and reversal evidence.

## Guardrails

- Never fabricate customer insight, market facts, proof, scarcity, urgency, testimonials, or benchmarks.
- A framework suggests a lens; it does not prove what is true in the user's market.
