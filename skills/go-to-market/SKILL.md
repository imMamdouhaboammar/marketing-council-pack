---
name: go-to-market
description: Use when launching a new product, entering a market, adding a segment, changing sales motion, or deciding the initial audience, positioning, channels, offer, distribution, and launch sequence.
---

# Go To Market

**Goal:** Select a practical entry path that connects product truth, reachable demand, distribution, and economics.

## Process

1. Define entry objective, geography, segment, time horizon, and constraints.
2. Validate product readiness and distribution/fulfillment readiness.
3. Choose the initial buying situation and audience based on evidence and reachability.
4. Set category frame, value proposition, proof, and offer.
5. Choose channels by role in discovery, evaluation, response, sales assist, and retention.
6. Sequence launch experiments before irreversible scale.

## Council roles

- `../../agents/market-architect.md`
- `../../agents/product-marketing-director.md`
- `../../agents/channel-strategist.md`
- `../../agents/commercial-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Principles: `target-attractiveness-fit`, `physical-availability`, `product-demonstration`
- Applied theories: `stp`, `physical-availability`, `product-demonstration`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
