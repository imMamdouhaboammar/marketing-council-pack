---
name: media-strategy
description: Use when the user needs paid, owned, earned, creator, partnership, search, social, retail, marketplace, event, or sales-assisted channel planning, budget allocation, or channel-role decisions.
license: MIT
metadata:
  version: "1.3.0"
---

# Media Strategy

**Goal:** Assign channels according to audience behavior, reach, intent, economics, creative fit, and measurability.

## Process

1. Define channel jobs: create demand, capture demand, educate, convert, assist sales, or retain.
2. Estimate reachable audience and buying intent by channel.
3. Compare marginal cost and expected contribution, not only historical averages.
4. Check creative, data, sales, and operational requirements.
5. Protect enough budget for a test to generate interpretable evidence.
6. Define incrementality or contribution logic and reallocation rules.

## Council roles

- `../../agents/channel-strategist.md`
- `../../agents/brand-growth-strategist.md`
- `../../agents/commercial-strategist.md`

## Neural connections

- Principles: `mental-availability`, `physical-availability`, `long-short-horizons`
- Applied theories: `mental-availability`, `long-short-effects`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
