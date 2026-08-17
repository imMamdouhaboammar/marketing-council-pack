---
name: marketing-measurement
description: Use when the user needs KPI design, attribution review, experiment planning, incrementality, causal reasoning, measurement trees, success thresholds, or a decision about what evidence should govern marketing.
---

# Marketing Measurement

**Goal:** Turn marketing activity into a measurement tree with causal claims, decision thresholds, and evidence quality labels.

## Process

1. Name the decision and the evidence available.
2. Activate only theories that explain the observed constraint.
3. Compare at least one credible counterweight when the choice is strategic.
4. Produce one primary recommendation with mechanism, trade-off, and measurement.
5. State what evidence would reverse the recommendation.

## Council roles

- `../../agents/measurement-strategist.md`
- `../../agents/effectiveness-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Applied theories: `scientific-advertising`, `long-short-effects`, `causal-mechanism`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Challenge with `../../hooks/theory-fit-gate.md` and `../../hooks/causal-mechanism-check.md` when theory choice or causality is load-bearing.

## Required output

Return the decision, supporting evidence, assumptions, selected theory or mechanism, rejected alternative, measurement, confidence, and reversal evidence.

## Guardrails

- Never fabricate customer insight, market facts, proof, scarcity, urgency, testimonials, or benchmarks.
- A framework suggests a lens; it does not prove what is true in the user's market.
