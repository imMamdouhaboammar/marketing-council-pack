---
name: commerce-media-strategy
description: Use when retailer media, marketplaces, retail networks, social commerce, delivery apps, closed-loop purchase data, or shopper marketing affect channel allocation or measurement.
---

# Commerce Media Strategy

**Goal:** Evaluate commerce media on access, inventory, data, customer experience, economics, and incremental business impact.

## Process

1. Name the commercial decision and classify current facts as evidence, inference, assumption, or unknown.
2. Run the relevant 2026 freshness card before relying on platform behavior.
3. Activate only the theories that explain the observed constraint.
4. Compare a timeless marketing counterweight when the recommendation could become platform-biased.
5. Produce one primary decision with authority boundary, mechanism, measurement, and reversal evidence.

## Council roles

- `../../agents/commerce-media-strategist.md`
- `../../agents/channel-strategist.md`
- `../../agents/measurement-strategist.md`

## Neural connections

- Applied theories: `commerce-media-incrementality`, `closed-loop-bias`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Hooks: `../../hooks/closed-loop-bias-check.md`, `../../hooks/incrementality-required.md`, `../../hooks/commercial-reality-check.md`
- Current-state evidence lives under `../../references/2026/`; verify it when platform behavior is load-bearing.

## Required output

Return the decision, current evidence, enduring principle, selected theory, rejected alternative, authority boundary if automation is involved, measurement, confidence, and reversal evidence.

## Guardrails

- Do not treat a platform recommendation, attribution report, AI-generated answer, or closed-loop sale as causal proof by itself.
- Do not fabricate current platform availability, customer insight, product facts, performance claims, or policy requirements.
