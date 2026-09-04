<!--
doc_status: HISTORICAL_COMPLETED
created: 2026-08-17
last_reviewed: 2026-09-04
completed_by_release: v1.2.0
source_of_truth: false
-->

![Status: HISTORICAL_COMPLETED](https://img.shields.io/badge/status-historical__completed-6b7280)

> [!NOTE]
> **Historical implementation plan**
>
> Status: `HISTORICAL_COMPLETED`
>
> Completed by release: `v1.2.0`
>
> This file records the v1.2 neural-graph execution plan. The current routing architecture extends this work and is documented elsewhere
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> Do not execute this plan as a current task list

# Marketing Council v1.2.0 Neural Graph Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an executable marketing knowledge graph that connects marketing figures, schools, principles, theories, hooks, agents, and skills, while expanding missing specialist coverage.

**Architecture:** Keep Agent Skills as the portable runtime. Add a dependency-free JSON knowledge graph and deterministic router, then connect each agent/skill/hook to that graph through explicit sections and file-backed nodes.

**Tech Stack:** Markdown Agent Skills, JSON, Python standard library, unittest, deterministic ZIP packaging.

## Global Constraints

- Release version is 1.2.0.
- No celebrity personality imitation.
- All theory cards state applicability, limits, applied use, and counterweights.
- Graph validation has no third-party dependency.
- Host packages remain deterministic.
- OpenAI plugin remains skills-only.

---

### Task 1: Contract tests for v1.2
- [ ] Write failing tests for 20 skills, 18 agents, neural graph integrity, routing, and connection sections.
- [ ] Run tests and confirm expected failures.

### Task 2: Knowledge graph and router
- [ ] Add graph schema, signals, graph data, router documentation, router script, and graph validator.
- [ ] Make neural graph tests pass.

### Task 3: Figures, schools, principles, and theories
- [ ] Add reference cards and source registry entries.
- [ ] Add counterweights and applied-use guidance.
- [ ] Make reference integrity tests pass.

### Task 4: Agents and focused skills
- [ ] Add six specialist agents and six focused skills.
- [ ] Add neural connection sections to every agent and skill.
- [ ] Add OpenAI metadata for every new skill.

### Task 5: Hooks and council routing
- [ ] Upgrade existing hooks to emit normalized signals.
- [ ] Add theory-fit, school-conflict, causal-mechanism, category-maturity, decision-stage, and horizon gates.
- [ ] Update the main Council skill and Council Director to use the graph.

### Task 6: Distribution and docs
- [ ] Bump manifests and metadata to 1.2.0.
- [ ] Update README, changelog, validators, counts, and package tests.
- [ ] Build archives twice and verify deterministic hashes.

### Task 7: Final verification
- [ ] Run full unit suite.
- [ ] Run source and distribution validators.
- [ ] Build and validate OpenAI and Claude packages.
- [ ] Run Python compile and `git diff --check`.
