<!--
doc_status: HISTORICAL_COMPLETED
created: 2026-09-03
archived: 2026-09-04
last_reviewed: 2026-09-04
completed_by_release: v1.5.0
source_of_truth: false
-->

![Status: HISTORICAL_COMPLETED](https://img.shields.io/badge/status-historical__completed-6b7280)
![Release: v1.5.0](https://img.shields.io/badge/release-v1.5.0-173F35)

> [!NOTE]
> **Historical implementation plan**
>
> Status: `HISTORICAL_COMPLETED`
>
> Completed by release: `v1.5.0`
>
> This plan's implementation scope ended at a merge-ready PR. PR merge, OpenAI submission, approval, publication, and post-publication smoke tests are separate actions and are not represented as completed here
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
> - current tests, manifests, routing registries, and package validators
>
> Do not execute this plan as a current task list. Its unchecked boxes are preserved as historical planning state

# Omni Marketing Skill Packs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert all 29 Marketing Council Agent Skills into OmniSkill-pattern full packs with behavioral contracts, progressive disclosure, per-skill evals, deterministic validators, dynamic DAG routing, and submission-safe packaging.

**Architecture:** Preserve the existing 28-focused-plus-Council topology and current skill/neural routers. Add a shared full-pack contract and validator, local SkillSpecs/references/evals for every Skill, and a bounded dynamic DAG router for genuine cross-functional dependency chains. Keep host packaging separate from portable Skill behavior.

**Tech Stack:** Markdown, JSON, YAML, Python 3.12, unittest, GitHub Actions, OpenAI Agent Skills/Plugin packaging.

**Spec:** `docs/superpowers/specs/2026-09-03-omni-marketing-skill-packs-design.md`

## Global Constraints

- Base from `main` commit `8d522b18a0453aa0fbb937ca8390612afdce7716`.
- Work only on `feat/omni-marketing-skill-packs`.
- Target version is `1.5.0`.
- Preserve 29 total Skills: 28 focused plus `marketing-council`.
- Preserve skill router vs neural router separation.
- Add dynamic DAG routing as a distinct third layer.
- Every focused Skill must ship as a standalone complete pack.
- No Docker or Colima.
- No merge in this task; stop at merge-ready PR.

---

### Task 1: Define failing full-pack contract tests

**Files:**
- Create: `tests/test_omni_skill_packs.py`
- Create: `tests/test_dynamic_router.py`
- Modify: `.github/workflows/plugin-ci.yml`

**Produces:** executable RED gates for full-pack anatomy, SkillSpec completeness/domain specificity, local eval minimums, progressive disclosure, standalone bundle contents, and dynamic DAG behavior.

- [ ] Write tests that require every Skill to contain the design-specified full-pack files.
- [ ] Write tests that parse every `skill-spec.json` and validate required fields and workflow step contracts.
- [ ] Write tests that reject duplicated baseline-failure/workflow fingerprints across focused Skills.
- [ ] Write tests that require activation/behavior/pressure/regression local eval files and minimum case counts.
- [ ] Write dynamic-router tests for single focused ownership, Council fallback, two-step ordered DAG, parallel-safe group, collision fallback, and max-six bounded graph.
- [ ] Write submission-pack tests proving local SkillSpec/evals are in standalone ZIPs.
- [ ] Add CI steps for the new tests.
- [ ] Push and observe RED because production full packs/router do not exist yet.

### Task 2: Build shared Omni Marketing contract tooling

**Files:**
- Create: `references/skill-authoring/marketing-skill-contract.md`
- Create: `references/skill-authoring/evidence-policy.md`
- Create: `references/skill-authoring/evaluation-contract.md`
- Create: `scripts/validate_skill_packs.py`
- Create: `scripts/skill_bineval.py`
- Create: `scripts/evidence_ledger.py`

**Produces:** reusable contract and deterministic validators used by CI and all full packs.

- [ ] Implement structural parser/validator against the RED tests.
- [ ] Implement deterministic binary checks with evidence text and critical gate.
- [ ] Implement evidence-state normalization and validation.
- [ ] Run focused tests to GREEN before proceeding.

### Task 3: Render 28 domain-specific focused full packs

**Files:**
- Modify: `skills/<focused>/SKILL.md` for all 28 focused Skills.
- Create per focused Skill: `references/skill-spec.json`, `references/decision-model.md`, `references/failure-modes.md`, `references/output-contract.md`, `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, `evals/regression.yml`.

**Produces:** 28 self-contained domain-specific behavioral artifacts.

- [ ] Derive each Skill activation positives/negatives from the canonical route registry.
- [ ] Write unique observable baseline failures and collision sets.
- [ ] Define domain-specific workflow with action/why/freedom/evidence/completion.
- [ ] Define domain decision model and failure modes.
- [ ] Define observable output contract and completion conditions.
- [ ] Add local direct/implicit/negative activation evals and behavior/pressure/regression cases.
- [ ] Refactor each `SKILL.md` into a compact MOC with point-of-use reference directives.
- [ ] Run validator and uniqueness tests until GREEN.

### Task 4: Upgrade Council to an Omni meta-skill

**Files:**
- Modify: `skills/marketing-council/SKILL.md`
- Create: `skills/marketing-council/references/skill-spec.json`
- Create: `skills/marketing-council/references/decision-model.md`
- Create: `skills/marketing-council/references/failure-modes.md`
- Create: `skills/marketing-council/references/output-contract.md`
- Create: `skills/marketing-council/evals/*.yml`

**Produces:** full Council pack that owns ambiguous/cross-functional arbitration and delegates bounded work.

- [ ] Define Council-specific baseline failures, collisions, arbitration workflow, and completion gate.
- [ ] Keep the Skill router, dynamic router, and neural router conceptually separate.
- [ ] Point the MOC to local references and shared challenge/evidence assets.
- [ ] Run full-pack tests.

### Task 5: Implement bounded dynamic DAG routing

**Files:**
- Create: `routing/skill-handoffs.json`
- Create: `scripts/dynamic_router.py`
- Test: `tests/test_dynamic_router.py`

**Produces:** `route_dynamic(text) -> {mode, primary_skill, nodes, edges, parallel_groups, confidence, reason, fallback}`.

- [ ] Encode high-value before/after handoffs and parallel-safe relations from SkillSpecs.
- [ ] Reuse `skill_router.py` route evidence rather than reimplementing token scoring blindly.
- [ ] Build a 2-6 node graph only when distinct dependent decisions are explicitly present.
- [ ] Fall back to Council for collisions/ambiguity instead of inventing an order.
- [ ] Keep neural routing out of this planner.
- [ ] Run dynamic-router RED/GREEN cases.

### Task 6: Harden standalone packaging for full packs

**Files:**
- Modify: `tests/test_openai_submission_pack.py`
- Modify if required: `scripts/build_openai_submission_pack.py`

**Produces:** 29 standalone ZIPs carrying local SkillSpec, references, evals, metadata, and shared runtime dependencies.

- [ ] Assert every standalone ZIP contains local `references/skill-spec.json` and all four eval files.
- [ ] Assert Council ZIP embeds 28 focused full packs with their local contracts/evals.
- [ ] Build twice and verify deterministic outputs under existing packaging guarantees.

### Task 7: Release/configuration upgrade to v1.5.0

**Files:**
- Modify public manifests, listing metadata, adapters, README, CHANGELOG, release docs, CI.

**Produces:** one consistent source/submission version and truthful public capability description.

- [ ] Bump every public version surface to `1.5.0`.
- [ ] Document Omni-pattern full packs and three-layer routing without claiming publication.
- [ ] Keep 29/28 counts exact.
- [ ] Keep OpenAI snapshot/resubmission language explicit.

### Task 8: Verification, independent review, and PR

**Files:** none unless review finds valid defects.

**Produces:** merge-ready PR.

- [ ] Run full unit suite.
- [ ] Run `validate_skill_packs.py`.
- [ ] Run distribution validator.
- [ ] Build host packages.
- [ ] Build standalone OpenAI submission bundles.
- [ ] Validate clean extracted OpenAI package.
- [ ] Run Plugin Eval if the CLI is actually available; otherwise record it as unavailable rather than claiming a pass.
- [ ] Open PR to `main`.
- [ ] Request CodeRabbit review.
- [ ] Fix valid findings with fresh tests.
- [ ] Require final PR checks green and mergeable.
- [ ] Stop before merge.
