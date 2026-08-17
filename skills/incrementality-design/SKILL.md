---
name: incrementality-design
description: Use when the user needs to know what marketing caused, choose holdouts or geo tests, reconcile attribution with MMM, estimate incremental CAC or ROAS, or design a credible counterfactual.
---

# Incrementality Design

**Goal:** Choose the strongest feasible counterfactual method for the business decision and define thresholds before reading the result.

## Process

1. Name the commercial decision and classify current facts as evidence, inference, assumption, or unknown.
2. Run the relevant 2026 freshness card before relying on platform behavior.
3. Activate only the theories that explain the observed constraint.
4. Compare a timeless marketing counterweight when the recommendation could become platform-biased.
5. Produce one primary decision with authority boundary, mechanism, measurement, and reversal evidence.

## Council roles

- `../../agents/measurement-strategist.md`
- `../../agents/effectiveness-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Applied theories: `incrementality-ladder`, `closed-loop-bias`, `commerce-media-incrementality`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Hooks: `../../hooks/incrementality-required.md`, `../../hooks/causal-mechanism-check.md`, `../../hooks/closed-loop-bias-check.md`
- Current-state evidence lives under `../../references/2026/`; verify it when platform behavior is load-bearing.

## Required output

Return the decision, current evidence, enduring principle, selected theory, rejected alternative, authority boundary if automation is involved, measurement, confidence, and reversal evidence.

## Guardrails

- Do not treat a platform recommendation, attribution report, AI-generated answer, or closed-loop sale as causal proof by itself.
- Do not fabricate current platform availability, customer insight, product facts, performance claims, or policy requirements.
