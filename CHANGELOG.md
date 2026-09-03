# Changelog

## 1.5.0 - 2026-09-04

- Fully rendered all 29 Agent Skills as local behavioral and execution packs with decision, evidence, failure-mode, output, and eval artifacts.
- Added canonical execution bindings for all 28 focused Skills, mapping each to a primary specialist, skeptical counterweight, domain challenge gate, and evidence gate.
- Preserved three distinct routing layers: deterministic Skill Router, bounded Dynamic DAG Router, and post-ownership Neural Router.
- Fixed root routing metadata so `dynamic_router` points to `scripts/dynamic_router.py` instead of the single-Skill router.
- Hardened Council standalone packaging so all 28 embedded focused modules resolve agent, hook, routing, neural, and tool dependencies through bundle-local shared resources.
- Added renderer-drift, execution-binding, behavioral-eval, evidence-ledger, release-integrity, and standalone-package regression gates.
- Public OpenAI availability still requires a v1.5.0 submission or resubmission and fresh-chat verification after publication.

## 1.4.0 - 2026-09-03

- Fixed release-version drift that could leave the public ChatGPT/Codex plugin on an older submitted skill snapshot while GitHub contained newer skills.
- Added a canonical dynamic skill router covering every focused Marketing Council skill with `marketing-council` as the conservative fallback for ambiguous or cross-functional requests.
- Separated capability routing (`scripts/skill_router.py`) from the existing neural theory/agent router (`scripts/neural_router.py`).
- Updated the main Marketing Council skill to route narrow requests directly to one focused skill and use the full council only when arbitration is needed.
- Added release regression tests for 29-skill discovery metadata, route coverage, version consistency, explicit/implicit invocation contracts, and built OpenAI package completeness.
- Added GitHub Actions verification for unit tests, distribution validation, deterministic package builds, and OpenAI plugin preflight.
- Added an OpenAI release runbook explaining public skill snapshots, version bumps, resubmission, and post-publication smoke tests.
- Updated OpenAI, Claude, root, and submission metadata to version 1.4.0.

## 1.3.0 - 2026-08-17

- Added six specialist agents for AI discovery, agentic commerce, marketing automation governance, signal architecture, creator commerce, and commerce media.
- Added nine focused skills for AI discovery, conversational advertising, agentic commerce, commerce feed intelligence, autonomous media operations, signal strategy, incrementality, creator commerce, and commerce media.
- Added ten challenge hooks for AI surfaces, agentic readiness, feed quality, signal quality, automation authority, black-box risk, incrementality, creative provenance, creator measurement, and closed-loop bias.
- Added five modern schools, fourteen principles, sixteen applied theories, twenty-one diagnostic signals, and six dated 2026 evidence nodes.
- Added primary-source 2026 evidence cards for Google, TikTok, Meta, and IAB developments while keeping platform facts separate from timeless marketing principles.
- Upgraded measurement, creative, channel, product marketing, effectiveness, and council orchestration for AI-mediated marketing decisions.

## 1.2.0 - 2026-08-17

- Added an executable neural marketing knowledge graph with 380 explicit connections.
- Added 25 figure cards, 14 school cards, 30 principle cards, and 30 applied-theory cards.
- Expanded the council to 18 specialist agents and 20 focused skills.
- Added brand equity, creative, effectiveness, competitive strategy, lifecycle, and measurement specialists.
- Added brand strategy, product marketing, segmentation, category strategy, behavioral marketing, and measurement skills.
- Added six new challenge hooks for theory fit, school conflict, causal mechanism, category maturity, decision stage, and horizon balance.
- Added deterministic neural routing and graph validation scripts.
- Added explicit neural connections to every agent, skill, and hook.
- Updated OpenAI/Codex, Claude Marketplace, portable skill, and source packaging.

## 1.1.0 - 2026-08-17

- Rebuilt the README as a product-first landing page with installation, examples, architecture, evals, and usage guidance.
- Added a native ChatGPT/Codex plugin manifest at `.codex-plugin/plugin.json`.
- Added a ChatGPT/Codex repository marketplace at `.agents/plugins/marketplace.json`.
- Added `agents/openai.yaml` metadata for all 14 Agent Skills.
- Added a native Claude plugin manifest and Claude marketplace metadata.
- Converted all 12 specialist role files into valid Claude subagent definitions while keeping them usable as shared role documents on other hosts.
- Added current Skills CLI installation commands for all agents, Codex, Claude Code, single-skill installs, listing, direct use, and updates.
- Added square plugin identity assets for install surfaces.
- Added deterministic host package generation for OpenAI, Claude, the self-contained skill, and the full source pack.
- Added host-distribution validation and deterministic archive checks.
- Updated host adapter documentation and submission listing metadata.

## 1.0.0 - 2026-08-17

- Added the Marketing Council orchestrator skill.
- Added 12 specialist council role cards.
- Added 13 focused marketing skills.
- Added evidence, freshness, commercial, customer-language, pre-mortem, and red-team hooks.
- Added full-strategy, launch, campaign, audit, and council-debate workflows.
- Added source-attributed marketing canon cards and decision references.
- Added deterministic unit-economics, funnel, experiment, tactic-ranking, and strategy-lint utilities.
- Added generic, Claude, OpenAI/ChatGPT/Codex, and GitHub Copilot adapter guidance.
- Added a self-contained distribution builder.
- Added scenario and adversarial eval suites.
