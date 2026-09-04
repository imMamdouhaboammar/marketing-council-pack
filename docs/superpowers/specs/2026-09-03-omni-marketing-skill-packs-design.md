<!--
doc_status: HISTORICAL_COMPLETED
created: 2026-09-03
last_reviewed: 2026-09-04
completed_by_release: v1.5.0
source_of_truth: false
-->

![Status: HISTORICAL_COMPLETED](https://img.shields.io/badge/status-historical__completed-6b7280)

> [!NOTE]
> **Historical completed design**
>
> Status: `HISTORICAL_COMPLETED`
>
> Completed by release: `v1.5.0`
>
> This design drove the Omni full-pack implementation and is preserved as engineering history. Post-design hardening added stricter declared-handoff validation, complete parallel DAG tails, symlink rejection in release builders, bundle-local SkillSpec path rewriting, and an evidence-bound submission draft
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> Treat the implementation and current tests as authoritative when they differ from this design

# Omni Marketing Skill Packs Design

## Goal

Upgrade Marketing Council from a well-packaged collection of mostly thin marketing prompts into a behaviorally specified, testable, progressively disclosed library of 29 full Agent Skill packs while preserving the v1.4 discovery and standalone-submission guarantees.

## Baseline

The repository currently has 28 focused Skills plus `marketing-council`, deterministic skill routing, a separate neural/theory router, specialist agents, shared references/hooks/tools, OpenAI metadata, standalone submission packaging, and green package-level CI.

The focused Skills are not yet OmniSkill-grade behavioral artifacts. Most focused Skills expose a short goal, a generic process, role links, neural links, one output paragraph, and generic guardrails. They generally lack a local SkillSpec, explicit baseline failures, activation collision boundaries, step freedom calibration, local progressive references, per-skill behavior/pressure evals, and completion/failure contracts.

## Design principles

1. Treat every Skill as a tested behavioral artifact, not a long prompt.
2. Keep `SKILL.md` as a Map of Content. Put domain depth in local references and machine-readable contracts.
3. Preserve one recognizable user job per focused Skill.
4. Define activation positives, implicit positives, near-miss negatives, and collision Skills.
5. Define observable baseline failures before writing behavior rules.
6. Define workflow steps as action + why + freedom (`low`, `medium`, `high`).
7. Define evidence states and never silently upgrade assumptions into facts.
8. Put deterministic checks/calculations in scripts where practical.
9. Give every focused Skill local eval coverage for activation, behavior, pressure, and regression.
10. Preserve host-neutral core behavior and keep OpenAI/Claude/Codex packaging concerns in adapters/builders.
11. Keep the existing skill router separate from the neural router.
12. Add a third routing layer for dynamic multi-skill execution: a handoff/DAG router that orders focused Skills only when a request genuinely spans dependent decisions.
13. Unknown or cross-functional requests continue to fall back to `marketing-council`.
14. A full pack must remain standalone after OpenAI submission packaging.

## Full-pack anatomy

Every focused Skill must contain:

```text
skills/<slug>/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── skill-spec.json
│   ├── decision-model.md
│   ├── failure-modes.md
│   └── output-contract.md
└── evals/
    ├── activation.yml
    ├── behavior.yml
    ├── pressure.yml
    └── regression.yml
```

Local scripts are optional and only added when the domain has a deterministic mechanic that is materially safer than free-form reasoning. Shared deterministic helpers remain under `scripts/` and are copied into standalone bundles by the existing packager.

`marketing-council` is a meta-skill. It must contain the same local contracts plus Council-specific routing and synthesis references. Its standalone ZIP must continue embedding all focused modules.

## SkillSpec contract

Each `references/skill-spec.json` must declare:

- `name`
- `purpose`
- `baseline_failures`
- `activation.positive`
- `activation.implicit`
- `activation.negative`
- `activation.collisions`
- `outputs`
- `invariants`
- `non_goals`
- `workflow[]` with `id`, `action`, `why`, `freedom`, `evidence_required`, `completion`
- `capabilities.required|optional|not_allowed`
- `evidence_policy`
- `failure_behavior`
- `completion_conditions`
- `handoffs.before|after`
- `host_targets`
- `eval_files`

Focused SkillSpecs must be meaningfully domain-specific. Reusing the same baseline failures, workflow, or output schema across unrelated Skills is a validation failure.

## Progressive disclosure

Focused `SKILL.md` files should remain compact and imperative. They should contain:

- purpose/activation boundary
- preflight/evidence rule
- a decision-flow summary
- point-of-use directives to local references
- deterministic helper pointers when relevant
- handoff rules
- completion gate

Detailed taxonomies, decision trees, examples, failure analysis, and output schemas belong in `references/`.

## Dynamic routing architecture

Three distinct layers must exist:

1. `skill_router.py`: select one primary focused Skill or Council fallback from request intent.
2. `dynamic_router.py`: construct an ordered DAG when multiple dependent marketing decisions are requested. It uses explicit handoff rules, route evidence, and collision boundaries. It must not turn every broad request into all 28 Skills.
3. `neural_router.py`: after ownership is established, rank theories, schools, principles, and specialist agents.

Dynamic router output must include:

- `mode`: `focused`, `council`, or `dag`
- `primary_skill`
- `nodes[]`
- `edges[]`
- `parallel_groups[]`
- `reason`
- `confidence`
- `fallback`

A DAG may contain 2-6 focused Skills by default. More than 6 requires explicit evidence that each node changes a decision.

## Evaluation architecture

Each focused Skill gets at least:

- 3 direct activation cases
- 3 implicit activation cases
- 3 near-miss negatives
- 3 behavioral assertions
- 2 pressure/adversarial cases
- 1 regression case

The repository adds deterministic structural validation and a binary evaluation contract. Structural gates are blocking. LLM-judged quality is represented as evidence when a compatible evaluator exists and must not be fabricated.

The validator must check:

- full-pack files exist
- SkillSpec schema completeness
- at least 3 positive, 3 implicit, 2 negative triggers
- collision set present
- unique/domain-specific baseline failures
- workflow freedom values valid
- every workflow step has action/why/evidence/completion
- declared eval files exist
- SKILL.md points to local references at point of use
- SKILL.md stays below the configured size ceiling
- no absolute user paths or secret-shaped content
- all local references resolve
- dynamic handoff targets are valid Skills
- standalone bundles contain local references/evals/specs

## Tooling

Add shared deterministic tooling:

- `scripts/validate_skill_packs.py`: full-pack structural and contract validator
- `scripts/dynamic_router.py`: ordered multi-skill DAG planner
- `scripts/skill_bineval.py`: deterministic binary questions over pack structure/contracts
- `scripts/evidence_ledger.py`: normalize FACT/EVIDENCE/INFERENCE/ASSUMPTION/HYPOTHESIS/UNKNOWN records

Existing domain tools remain and are referenced by relevant Skills rather than duplicated.

## Domain specialization

Every focused Skill receives a distinct decision model. Examples:

- pricing: economic floor, value/reference frame, packaging logic, consequence ranges, rollout thresholds
- positioning: competitive alternatives, category frame, differentiated value, proof, falsification
- media: channel job, reach/frequency economics, marginal reach, budget logic, incrementality boundary
- conversion: funnel denominator, friction taxonomy, intent-stage diagnosis, instrumentation gate
- retention: retention curve/cohort diagnosis, churn mechanism, intervention economics, holdout/measurement
- incrementality: counterfactual ladder, contamination, feasibility, pre-registration, causal decision thresholds
- creator commerce: creator role, audience/creative/affiliate/commerce separation, economics, measurement/disclosure boundaries

## Packaging

The current OpenAI submission builder already copies local Skill child directories. Tests must prove that `references/skill-spec.json` and local `evals/` survive in every standalone Skill archive, and that Council still embeds all 28 focused full packs.

## Versioning

This is a public behavioral change and requires a new release version. Target version: `1.5.0`.

All public manifests, adapters, listing metadata, README badges, changelog, and release docs must agree on `1.5.0`. A future OpenAI publication still requires a fresh submission snapshot after merge.

## Security and safety

- No credentials or hardcoded private paths in Skills or references.
- Tools describe capabilities, not imaginary permissions.
- Research-dependent claims retain freshness requirements.
- Deterministic scripts consume data and produce analysis only; they do not mutate third-party services.
- Marketing ethics guardrails remain: no fabricated proof, customer insight, urgency, scarcity, performance claims, or causal certainty.

## Acceptance gates

A branch is merge-ready only when:

1. all 29 Skills satisfy the full-pack validator;
2. all 28 focused Skills have distinct SkillSpecs and local eval suites;
3. dynamic routing regression tests pass for focused, Council fallback, ordered DAG, collisions, and bounded node count;
4. existing neural routing and v1.4 discovery tests remain green;
5. full unit suite passes;
6. distribution validation passes;
7. host packages build;
8. 29 standalone OpenAI Skill bundles build;
9. extracted OpenAI package validates;
10. CodeRabbit review has no unresolved valid blocking finding;
11. PR is mergeable and checks are green;
12. no merge is executed without a later explicit user instruction.
