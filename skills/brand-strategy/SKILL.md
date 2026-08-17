---
name: brand-strategy
description: Use when the user needs brand strategy, brand memory, distinctive assets, brand associations, salience, brand architecture, or a decision about how brand building supports growth.
---

# Brand Strategy

**Goal:** Build a brand decision around memory, meaning, distinctive recognition, and observable buying behavior.

## Process

1. Name the decision and the evidence available.
2. Activate only theories that explain the observed constraint.
3. Compare at least one credible counterweight when the choice is strategic.
4. Produce one primary recommendation with mechanism, trade-off, and measurement.
5. State what evidence would reverse the recommendation.

## Council roles

- `../../agents/brand-equity-strategist.md`
- `../../agents/brand-growth-strategist.md`
- `../../agents/creative-strategist.md`

## Neural connections

- Applied theories: `brand-equity-model`, `customer-based-brand-equity`, `mental-availability`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Challenge with `../../hooks/theory-fit-gate.md` and `../../hooks/causal-mechanism-check.md` when theory choice or causality is load-bearing.

## Required output

Return the decision, supporting evidence, assumptions, selected theory or mechanism, rejected alternative, measurement, confidence, and reversal evidence.

## Guardrails

- Never fabricate customer insight, market facts, proof, scarcity, urgency, testimonials, or benchmarks.
- A framework suggests a lens; it does not prove what is true in the user's market.
