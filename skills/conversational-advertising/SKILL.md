---
name: conversational-advertising
description: Use when the user needs strategy for ads embedded in conversational search, AI-assisted comparison, business chat agents, dynamic offers, or other answer-like paid experiences.
license: MIT
metadata:
  version: "1.3.0"
---

# Conversational Advertising

**Goal:** Design paid interventions that answer a real decision question, preserve sponsorship clarity, and connect conversation to proof, offer, and next action.

## Process

1. Name the commercial decision and classify current facts as evidence, inference, assumption, or unknown.
2. Run the relevant 2026 freshness card before relying on platform behavior.
3. Activate only the theories that explain the observed constraint.
4. Compare a timeless marketing counterweight when the recommendation could become platform-biased.
5. Produce one primary decision with authority boundary, mechanism, measurement, and reversal evidence.

## Council roles

- `../../agents/ai-discovery-strategist.md`
- `../../agents/response-strategist.md`
- `../../agents/channel-strategist.md`

## Neural connections

- Applied theories: `conversational-intent-matching`, `ai-mediated-discovery`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Hooks: `../../hooks/ai-surface-check.md`, `../../hooks/freshness-check.md`, `../../hooks/commercial-reality-check.md`
- Current-state evidence lives under `../../references/2026/`; verify it when platform behavior is load-bearing.

## Required output

Return the decision, current evidence, enduring principle, selected theory, rejected alternative, authority boundary if automation is involved, measurement, confidence, and reversal evidence.

## Guardrails

- Do not treat a platform recommendation, attribution report, AI-generated answer, or closed-loop sale as causal proof by itself.
- Do not fabricate current platform availability, customer insight, product facts, performance claims, or policy requirements.
