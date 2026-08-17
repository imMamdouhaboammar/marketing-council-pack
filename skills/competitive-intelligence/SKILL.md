---
name: competitive-intelligence
description: Use when marketing strategy depends on current competitors, category claims, prices, offers, channels, reviews, positioning, product changes, share of voice, or alternative solutions.
---

# Competitive Intelligence

**Goal:** Build a current evidence-based view of competitive alternatives without copying competitor activity.

## Process

1. Define the buyer alternatives, not only named direct competitors.
2. Use current sources for prices, offers, product claims, availability, and channel behavior.
3. Separate competitor facts from inferred strategy.
4. Compare category frame, proposition, proof, price, experience, distribution, and customer complaints.
5. Identify white space only when it matters to buyer choice and the company can credibly occupy it.
6. Use intelligence to improve a decision, not to produce a feature matrix for its own sake.

## Council roles

- `../../agents/positioning-strategist.md`
- `../../agents/market-architect.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Principles: `competitive-structure`, `competitive-alternatives`, `evidence-status`
- Applied theories: `five-forces`, `positioning-components`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
