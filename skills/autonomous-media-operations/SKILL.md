---
name: autonomous-media-operations
description: Use when AI assistants, platform automation, marketing agents, automated bidding, budgeting, targeting, or campaign creation can materially change spend or execution.
license: MIT
metadata:
  version: "1.3.0"
---

# Autonomous Media Operations

**Goal:** Define the authority matrix, objectives, guardrails, review cadence, exception handling, auditability, and rollback rules for AI-assisted media.

## Process

1. Name the commercial decision and classify current facts as evidence, inference, assumption, or unknown.
2. Run the relevant 2026 freshness card before relying on platform behavior.
3. Activate only the theories that explain the observed constraint.
4. Compare a timeless marketing counterweight when the recommendation could become platform-biased.
5. Produce one primary decision with authority boundary, mechanism, measurement, and reversal evidence.

## Council roles

- `../../agents/marketing-automation-governor.md`
- `../../agents/channel-strategist.md`
- `../../agents/measurement-strategist.md`

## Neural connections

- Applied theories: `automation-decision-rights`, `autonomous-media-governance`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Hooks: `../../hooks/automation-authority-check.md`, `../../hooks/automation-black-box-check.md`, `../../hooks/commercial-reality-check.md`
- Current-state evidence lives under `../../references/2026/`; verify it when platform behavior is load-bearing.

## Required output

Return the decision, current evidence, enduring principle, selected theory, rejected alternative, authority boundary if automation is involved, measurement, confidence, and reversal evidence.

## Guardrails

- Do not treat a platform recommendation, attribution report, AI-generated answer, or closed-loop sale as causal proof by itself.
- Do not fabricate current platform availability, customer insight, product facts, performance claims, or policy requirements.
