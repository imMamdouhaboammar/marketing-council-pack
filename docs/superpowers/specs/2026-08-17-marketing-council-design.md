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
> This initial design records the v1.0-era architecture. The current product has expanded to 29 full Skill packs, three routing layers, execution bindings, and hardened release packaging
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> **Superseded assumptions:** the original role/Skill inventory, pre-neural routing architecture, and pre-v1.5 packaging model
>
> **Do not execute this document directly.** Reconcile any historical instruction against the current repository, tests, and architecture first

# Marketing Council Skill Pack Design

## Goal
Build a portable agent-skill pack that helps AI agents make marketing strategy and tactic decisions using explicit marketing schools, evidence, commercial constraints, adversarial review, and measurable execution rather than celebrity role-play.

## Design principles

1. Do not imitate named marketers. Extract decision principles and apply them only when the situation fits.
2. Separate knowledge, decision roles, orchestration, deterministic calculation, host integration, and evaluation.
3. Diagnose before prescribing tactics.
4. Tag strategic claims as fact, evidence, inference, assumption, hypothesis, or unknown.
5. Require current research for time-sensitive market, competitor, platform, policy, pricing, and benchmark claims.
6. Make disagreement explicit. The council director resolves conflicts using evidence, economics, constraints, and time horizon.
7. Preserve progressive disclosure: main SKILL.md files stay concise; detailed material lives in references.
8. Keep the core host-neutral. Claude, Codex/OpenAI, Copilot, and generic agents receive adapters rather than duplicated logic.
9. Use deterministic scripts for arithmetic, scoring, and linting.
10. Evaluate behavior on materially different marketing cases and adversarial prompts.

## Core roles

- council-director: task triage, dispatch, synthesis, conflict resolution, final decision
- market-architect: market definition, segmentation, targeting, demand, route-to-market
- positioning-strategist: category, alternatives, differentiation, memory structures
- audience-strategist: buying situations, JTBD, motivations, anxieties, customer language
- product-marketing-director: product truth, prioritization, demonstration, launch narrative
- response-strategist: offer, proof, specificity, objection handling, response mechanics
- awareness-strategist: awareness and sophistication state, message depth, proof burden
- behavior-strategist: friction, risk, social proof, choice architecture, ethical behavioral cues
- brand-growth-strategist: penetration, reach, availability, distinctive assets, short/long horizon
- commercial-strategist: price, margin, CAC, LTV, payback, capacity, contribution economics
- channel-strategist: channel selection by intent, reach, economics, fit, and measurability
- marketing-skeptic: red team, falsification, unsupported assumptions, pre-mortem

## Main flow

UNDERSTAND -> DIAGNOSE -> RESEARCH -> DISPATCH -> DEBATE -> CHALLENGE -> DECIDE -> PLAN -> EXECUTE -> MEASURE -> LEARN

## Output contracts

A full strategy includes situation, problem, evidence, diagnosis, audience, positioning, value proposition, strategic choice, exclusions, channels, offer, messaging, tactics, experiments, measurement, risks, assumptions, and next decisions.

Every tactic includes objective, audience, insight, mechanism, message, channel, customer action, expected effect, evidence, cost, effort, risk, measurement, success threshold, failure threshold, and next action.

## Portability

Use the Agent Skills `SKILL.md` format as the portable authoring format. Keep adapters for host-specific discovery/install paths and plugin manifests. Avoid host-specific tools inside core instructions; instead define capability contracts such as web search, files, analytics, ads, CRM, spreadsheet, experiment math, and browser inspection.

## Testing

Validate frontmatter, file references, script behavior, arithmetic, tactic ranking, strategy lint rules, and at least eight scenario evals. Include adversarial evals for generic tactics, unsupported claims, requested-channel bias, vanity metrics, and stale market assumptions.
