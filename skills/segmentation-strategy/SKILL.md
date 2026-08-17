---
name: segmentation-strategy
description: Use when the user needs segmentation, target selection, ICP design, audience prioritization, or a decision about whether market differences are meaningful enough to change marketing.
---

# Segmentation Strategy

**Goal:** Create decision-useful segments and choose a reachable, valuable target without confusing demographics with motivation.

## Process

1. Name the decision and the evidence available.
2. Activate only theories that explain the observed constraint.
3. Compare at least one credible counterweight when the choice is strategic.
4. Produce one primary recommendation with mechanism, trade-off, and measurement.
5. State what evidence would reverse the recommendation.

## Council roles

- `../../agents/market-architect.md`
- `../../agents/audience-strategist.md`
- `../../agents/commercial-strategist.md`

## Neural connections

- Applied theories: `stp`, `jobs-to-be-done`, `smallest-viable-audience`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Challenge with `../../hooks/theory-fit-gate.md` and `../../hooks/causal-mechanism-check.md` when theory choice or causality is load-bearing.

## Required output

Return the decision, supporting evidence, assumptions, selected theory or mechanism, rejected alternative, measurement, confidence, and reversal evidence.

## Guardrails

- Never fabricate customer insight, market facts, proof, scarcity, urgency, testimonials, or benchmarks.
- A framework suggests a lens; it does not prove what is true in the user's market.
