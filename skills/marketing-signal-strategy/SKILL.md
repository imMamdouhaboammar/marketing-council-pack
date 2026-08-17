---
name: marketing-signal-strategy
description: Use when campaign or lifecycle optimization depends on CRM outcomes, lead quality, margin, offline conversions, delayed revenue, first-party data, or noisy proxy events.
license: MIT
metadata:
  version: "1.3.0"
---

# Marketing Signal Strategy

**Goal:** Design which business signals should steer marketing automation, with explicit value, latency, bias, confidence, and eligibility.

## Process

1. Name the commercial decision and classify current facts as evidence, inference, assumption, or unknown.
2. Run the relevant 2026 freshness card before relying on platform behavior.
3. Activate only the theories that explain the observed constraint.
4. Compare a timeless marketing counterweight when the recommendation could become platform-biased.
5. Produce one primary decision with authority boundary, mechanism, measurement, and reversal evidence.

## Council roles

- `../../agents/marketing-signal-architect.md`
- `../../agents/measurement-strategist.md`
- `../../agents/commercial-strategist.md`

## Neural connections

- Applied theories: `marketing-signal-architecture`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Hooks: `../../hooks/marketing-signal-quality.md`, `../../hooks/causal-mechanism-check.md`, `../../hooks/freshness-check.md`
- Current-state evidence lives under `../../references/2026/`; verify it when platform behavior is load-bearing.

## Required output

Return the decision, current evidence, enduring principle, selected theory, rejected alternative, authority boundary if automation is involved, measurement, confidence, and reversal evidence.

## Guardrails

- Do not treat a platform recommendation, attribution report, AI-generated answer, or closed-loop sale as causal proof by itself.
- Do not fabricate current platform availability, customer insight, product facts, performance claims, or policy requirements.
