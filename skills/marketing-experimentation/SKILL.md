---
name: marketing-experimentation
description: Use when the user needs to design decision-relevant marketing experiments with falsifiable hypotheses; route here only when this decision boundary is the clear owner.
---

# Marketing Experimentation

## Job

Design decision-relevant marketing experiments with falsifiable hypotheses

Own this request only when **experiment design** is the clear decision boundary. If ownership is ambiguous or several functions compete, route to `marketing-council`. If the user explicitly asks for dependent work across functions, use `../../scripts/dynamic_router.py` to build a bounded DAG.

## Operating contract

1. Read `references/skill-spec.json` first for activation, invariants, workflow freedom, evidence rules, handoffs, and completion conditions.
2. Use `references/decision-model.md` when framing or challenging the decision.
3. Check `references/failure-modes.md` before finalizing a recommendation.
4. Render the response against `references/output-contract.md`.
5. Use packaged shared references or current external research only when they are load-bearing. Never present inference as evidence.

## Evidence discipline

Classify material claims as fact, inference, assumption, or unknown. Prefer supplied primary evidence. Verify current platform, policy, product, pricing, or market claims when freshness affects the recommendation. Do not fabricate research, tool calls, metrics, customer language, or causal proof.

## Routing

- Focused request: stay inside this Skill.
- Ambiguous or cross-functional ownership: hand to `marketing-council`.
- Explicit dependency chain: use `../../scripts/dynamic_router.py`.
- After Skill ownership is known, theory/agent selection may use `../../scripts/neural_router.py`; neural nodes never replace Skill routing.

## Completion gate

Complete only when the decision is explicit, evidence and inference are separated, a credible alternative was considered, outputs are rendered, material uncertainty is stated, and measurement plus reversal evidence are defined.

Local behavioral evaluations live in `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, and `evals/regression.yml`.
