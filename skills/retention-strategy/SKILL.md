---
name: retention-strategy
description: Use when the user needs churn reduction, repeat purchase, lifecycle marketing, onboarding, activation, loyalty, win-back, customer communication, or a diagnosis of weak retention.
license: MIT
metadata:
  version: "1.3.0"
---

# Retention Strategy

**Goal:** Identify why customers fail to reach or repeat value and choose interventions that improve durable behavior.

## Process

1. Define the retained behavior and cohort window.
2. Separate acquisition quality from onboarding, product value, service, price, habit, and competitive causes.
3. Locate the point where expected value and experienced value diverge.
4. Prioritize product/service fixes before messaging when the experience itself is the cause.
5. Design lifecycle interventions around real moments and risks.
6. Judge impact on retention, contribution, and customer experience together.

## Council roles

- `../../agents/commercial-strategist.md`
- `../../agents/audience-strategist.md`
- `../../agents/behavior-strategist.md`
- `../../agents/product-marketing-director.md`

## Neural connections

- Principles: `jtbd-progress`, `permission-relevance`, `friction-before-motivation`
- Applied theories: `jobs-to-be-done`, `fogg-behavior-model`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
