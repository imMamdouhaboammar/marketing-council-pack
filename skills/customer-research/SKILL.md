---
name: customer-research
description: Use when marketing decisions require real customer motivations, buying triggers, objections, language, jobs, anxieties, decision roles, or evidence from interviews, reviews, calls, CRM, search, comments, or support data.
license: MIT
metadata:
  version: "1.3.0"
---

# Customer Research

**Goal:** Turn customer evidence into decision-ready patterns without inventing psychology.

## Process

1. Define the research question before collecting quotes.
2. Prefer behavior and buying situations over demographic stereotypes.
3. Separate user, buyer, approver, blocker, and beneficiary where relevant.
4. Cluster repeated triggers, desired progress, objections, alternatives, anxieties, and exact language.
5. Mark frequency and source quality; do not treat a vivid quote as prevalence.
6. Convert findings into implications for positioning, offer, messaging, product, or channel choice.

## Council roles

- `../../agents/audience-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Principles: `jtbd-progress`, `segmentation-decision-usefulness`, `evidence-status`
- Applied theories: `jobs-to-be-done`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
