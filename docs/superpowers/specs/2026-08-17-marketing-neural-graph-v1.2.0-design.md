<!--
doc_status: HISTORICAL_SUPERSEDED
created: 2026-08-17
last_reviewed: 2026-09-04
source_of_truth: false
-->

![Status: HISTORICAL_SUPERSEDED](https://img.shields.io/badge/status-historical__superseded-yellow)

> [!WARNING]
> **Superseded historical document**
>
> Status: `HISTORICAL_SUPERSEDED`
>
> This document records the v1.2 neural-graph design. The neural graph remains part of the product, but v1.5 separates Skill ownership, Dynamic DAG routing, and Neural routing into three explicit layers
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> **Superseded assumptions:** v1.2 component counts and the earlier routing model that predated the distinct Skill Router and Dynamic DAG Router
>
> **Do not execute this document directly.** Reconcile any historical instruction against the current repository, tests, and architecture first

# Marketing Council v1.2.0 Neural Knowledge Graph Design

## Goal

Turn Marketing Council from a set of coordinated marketing skills into an explicit executable knowledge graph that connects marketing figures, schools, principles, applied theories, signals, agents, skills, hooks, and counterweights.

## Architecture

The pack keeps Agent Skills as the portable execution unit. A new `neural/graph.json` becomes the machine-readable connection map. Hooks emit normalized signals, the router activates relevant theory/school nodes, those nodes route to agents and focused skills, and the Council Director synthesizes the outputs. The graph is advisory and deterministic routing support, not a claim that a single theory is universally correct.

## New specialist coverage

Add six missing roles:
- brand-equity-strategist
- creative-strategist
- effectiveness-strategist
- competitive-strategy-analyst
- lifecycle-strategist
- measurement-strategist

Add six focused skills:
- brand-strategy
- product-marketing
- segmentation-strategy
- category-strategy
- behavioral-marketing
- marketing-measurement

## Knowledge model

The graph supports node types: `figure`, `school`, `principle`, `theory`, `signal`, `agent`, `skill`, and `hook`.

Supported edge semantics include:
- `belongs_to`
- `informs`
- `operationalizes`
- `activates`
- `routes_to`
- `challenges`
- `counterbalances`
- `requires`
- `measured_by`
- `hands_off_to`

Every figure must inform at least one principle or school. Every theory must route to at least one skill or agent. Every agent and skill graph node must point to an existing file.

## Schools and figures

The v1.2 library expands beyond the original canon with customer-centric market definition, brand equity, competitive strategy, creative advertising, behavioral design, modern B2B/SaaS positioning, and marketing effectiveness. Figure cards describe principles and boundaries, not personality imitation.

## Routing signals

Hooks normalize observations into signals such as:
- evidence-quality-low
- economics-unhealthy
- category-mature
- category-unclear
- awareness-low
- awareness-high
- differentiation-weak
- behavioral-friction-high
- brand-memory-weak
- distribution-constraint
- retention-weak
- short-horizon
- long-horizon
- competitor-pressure-high

The router scores connected nodes and returns ranked agents, skills, theories, principles, and hooks.

## Safety and epistemic rules

- No figure is treated as an authority whose name settles a decision.
- Counterweights must be preserved when two schools imply different action.
- Historical frameworks cannot be used as evidence for current market facts.
- Behavioral influence must remain truthful and avoid fabricated scarcity, proof, or social signals.
- A theory can suggest a mechanism but does not prove causality in the user's market.

## Validation

Tests verify graph integrity, file links, source coverage, deterministic routing, upgraded agent/skill/hook connection sections, release counts, and deterministic host archives.
