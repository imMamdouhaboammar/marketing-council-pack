---
name: offer-strategy
description: Use when the user needs to create, diagnose, compare, or improve an offer, promotion, package, guarantee, proof structure, CTA, response mechanism, or objection-handling approach.
license: MIT
metadata:
  version: "1.3.0"
---

# Offer Strategy

**Goal:** Make the value exchange concrete, credible, and measurable.

## Process

1. Clarify who the offer is for and the buying situation.
2. Define what the buyer gets, pays, risks, and must do next.
3. Identify the dominant objection and the proof best suited to reduce it.
4. Check whether urgency or scarcity is factual before using it.
5. Check contribution economics and operational capacity.
6. Define the response event and business outcome that will judge the offer.

## Council roles

- `../../agents/response-strategist.md`
- `../../agents/behavior-strategist.md`
- `../../agents/commercial-strategist.md`

## Neural connections

- Principles: `proof-before-polish`, `performance-accountability`, `commercial-reality`
- Applied theories: `unique-selling-proposition`, `scientific-advertising`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
