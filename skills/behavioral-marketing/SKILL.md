---
name: behavioral-marketing
description: Use when the user needs behavioral diagnosis, choice architecture, friction reduction, prompts, social proof, defaults, framing, onboarding behavior, or conversion psychology grounded in truthful evidence.
license: MIT
metadata:
  version: "1.3.0"
---

# Behavioral Marketing

**Goal:** Diagnose the target behavior and change the environment, friction, prompt, or truthful decision cues before adding more persuasion.

## Process

1. Name the decision and the evidence available.
2. Activate only theories that explain the observed constraint.
3. Compare at least one credible counterweight when the choice is strategic.
4. Produce one primary recommendation with mechanism, trade-off, and measurement.
5. State what evidence would reverse the recommendation.

## Council roles

- `../../agents/behavior-strategist.md`
- `../../agents/lifecycle-strategist.md`
- `../../agents/measurement-strategist.md`

## Neural connections

- Applied theories: `fogg-behavior-model`, `influence-principles`, `nudge`, `behavioral-framing`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Challenge with `../../hooks/theory-fit-gate.md` and `../../hooks/causal-mechanism-check.md` when theory choice or causality is load-bearing.

## Required output

Return the decision, supporting evidence, assumptions, selected theory or mechanism, rejected alternative, measurement, confidence, and reversal evidence.

## Guardrails

- Never fabricate customer insight, market facts, proof, scarcity, urgency, testimonials, or benchmarks.
- A framework suggests a lens; it does not prove what is true in the user's market.
