---
name: marketing-experimentation
description: Use when the user needs an A/B test, marketing experiment, hypothesis, prioritization method, sample estimate, decision rule, test backlog, or a way to learn before committing more budget.
---

# Marketing Experimentation

**Goal:** Turn uncertain marketing beliefs into interpretable tests with explicit decision rules.

## Process

1. Write the claim as a falsifiable hypothesis.
2. Name the intervention and causal mechanism.
3. Choose one primary outcome and necessary guardrails.
4. Estimate the minimum effect worth detecting and required sample when possible.
5. Predefine success, failure, inconclusive, and stop rules.
6. Record what decision changes for each possible result.

## Council roles

- `../../agents/marketing-skeptic.md`
- `../../agents/commercial-strategist.md`

## Neural connections

- Principles: `performance-accountability`, `evidence-status`, `causal-mechanism`
- Applied theories: `scientific-advertising`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
