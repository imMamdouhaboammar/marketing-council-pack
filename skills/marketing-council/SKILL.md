---
name: marketing-council
description: Use when the user needs to diagnose ambiguous or cross-functional marketing problems and coordinate the minimum set of specialist skills; route here only when this decision boundary is the clear owner.
---

# Marketing Council

## Job

Diagnose ambiguous or cross-functional marketing problems and coordinate the minimum set of specialist skills

Own the request when the marketing problem is ambiguous or genuinely cross-functional. If one focused Skill clearly owns the next decision, delegate to that Skill instead of retaining Council ownership. If the request explicitly establishes dependent work across functions, use `../../scripts/dynamic_router.py` to build a bounded DAG.

## Operating contract

1. Read `references/skill-spec.json` first for activation, invariants, workflow freedom, evidence rules, handoffs, and completion conditions.
2. Use `references/decision-model.md` when framing or challenging the decision.
3. Check `references/failure-modes.md` before finalizing a recommendation.
4. Render the response against `references/output-contract.md`.
5. Use packaged shared references or current external research only when they are load-bearing. Never present inference as evidence.

## Evidence discipline

Classify material claims as fact, inference, assumption, or unknown. Prefer supplied primary evidence. Verify current platform, policy, product, pricing, or market claims when freshness affects the recommendation. Do not fabricate research, tool calls, metrics, customer language, or causal proof.

## Routing

- Single focused owner: delegate to the selected focused Skill.
- Ambiguous or cross-functional ownership: Council remains the diagnostic owner.
- Explicit dependency chain: use `../../scripts/dynamic_router.py` and keep the graph bounded to the minimum required Skills.
- After Skill ownership is known, theory/agent selection may use `../../scripts/neural_router.py`; neural nodes never replace Skill routing.

## Completion gate

Complete only when the decision is explicit, evidence and inference are separated, a credible alternative was considered, outputs are rendered, material uncertainty is stated, and measurement plus reversal evidence are defined.

Local behavioral evaluations live in `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, and `evals/regression.yml`.
