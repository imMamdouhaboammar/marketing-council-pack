---
name: conversion-strategy
description: Use when traffic or leads exist but conversion is weak, when the user needs CRO, funnel diagnosis, landing-page strategy, checkout improvements, lead-form changes, or experiment priorities.
---

# Conversion Strategy

**Goal:** Find and test the highest-value conversion constraint without mistaking persuasion for a fix to product or traffic quality.

## Process

1. Define the conversion event and qualified denominator.
2. Segment by source, device, intent, new/returning, and other meaningful behavior when data permits.
3. Identify friction, uncertainty, mismatch, weak proof, poor offer, technical defects, or low-quality traffic.
4. Prioritize evidence from analytics, sessions, research, and support rather than visual preference.
5. Define one hypothesis per experiment and the expected mechanism.
6. Set business and guardrail metrics before running the test.

## Council roles

- `../../agents/behavior-strategist.md`
- `../../agents/response-strategist.md`
- `../../agents/commercial-strategist.md`
- `../../agents/marketing-skeptic.md`

## Neural connections

- Principles: `friction-before-motivation`, `choice-architecture`, `proof-before-polish`
- Applied theories: `fogg-behavior-model`, `nudge`, `influence-principles`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.

## Required output

Return the decision, supporting evidence, assumptions, recommendation, rejected alternative, measurement, and evidence that would reverse the recommendation.

## Guardrails

- Never fabricate customer insight, research, proof, scarcity, urgency, or benchmarks.
- Research time-sensitive facts when current tools are available.
- If the requested tactic is not supported by the diagnosis, say so and propose the better decision.
