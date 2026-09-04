<!--
doc_status: ACTIVE
last_reviewed: 2026-09-04
release: 1.5.0
source_of_truth: false
-->

![Status: ACTIVE](https://img.shields.io/badge/status-ACTIVE-173F35)
![Release: v1.5.0](https://img.shields.io/badge/release-v1.5.0-173F35)

# Marketing Council Documentation

This is the canonical map for repository documentation. It tells maintainers and coding agents which documents are current, which work is still open, and which files are preserved only as engineering history

The live implementation, manifests, tests, routing registries, and current release metadata override historical plans when they disagree

## Start here

- **[ACTIVE]** [Repository README](../README.md) - current product architecture, Skill inventory, installation, routing, and execution model
- **[ACTIVE]** [OpenAI release runbook](OPENAI_RELEASE.md) - current packaging, submission, release, and post-publication contract
- **[ONGOING]** [OpenAI submission state](../submission/README.md) - current external submission inputs and verification boundary

## Current product documentation

- **[ACTIVE]** [Repository README](../README.md)
- **[ACTIVE]** [OpenAI release runbook](OPENAI_RELEASE.md)

Current implementation facts include 29 total Skills, 28 focused Skills, `marketing-council` fallback, 24 specialist agents, Skill Router, Dynamic DAG Router, Neural Router, execution bindings, local full-pack contracts/evals, fail-closed handoffs, symlink-safe builders, bundle-local SkillSpec paths, and evidence-bound submission material

## Ongoing work

- **[ONGOING]** [Submission and release pack](../submission/README.md) - required external portal identity, policy/support URLs, availability, submission, approval, publication, and fresh-host smoke tests

## Architecture and contracts

Authoritative machine-readable and executable contracts live outside historical plans:

- `routing/skill-routes.json`
- `routing/skill-handoffs.json`
- `routing/skill-execution-bindings.json`
- `scripts/skill_router.py`
- `scripts/dynamic_router.py`
- `scripts/neural_router.py`
- `scripts/validate_skill_packs.py`
- `scripts/validate_submission_pack.py`
- `skills/*/references/skill-spec.json`

## Release and distribution

- **[ACTIVE]** [OpenAI release runbook](OPENAI_RELEASE.md)
- **[ONGOING]** [Submission and release pack](../submission/README.md)
- `scripts/build_host_packages.py`
- `scripts/build_openai_submission_pack.py`
- `scripts/validate_distribution.py`
- `scripts/validate_openai_plugin.py`

## Historical specs

- **[HISTORICAL_SUPERSEDED]** [Initial Marketing Council design](superpowers/specs/2026-08-17-marketing-council-design.md)
- **[HISTORICAL_SUPERSEDED]** [v1.2 Neural Knowledge Graph design](superpowers/specs/2026-08-17-marketing-neural-graph-v1.2.0-design.md)
- **[HISTORICAL_COMPLETED]** [v1.5 Omni Marketing Skill Packs design](superpowers/specs/2026-09-03-omni-marketing-skill-packs-design.md)

Historical specs preserve the decisions and assumptions that existed when they were written. Do not treat them as the current product contract

## Historical implementation plans

- **[HISTORICAL_COMPLETED]** [Initial implementation plan](superpowers/plans/2026-08-17-marketing-council-implementation.md)
- **[HISTORICAL_COMPLETED]** [v1.1 distribution plan](superpowers/plans/2026-08-17-marketing-council-distribution-v1.1.md)
- **[HISTORICAL_COMPLETED]** [v1.2 neural graph plan](superpowers/plans/2026-08-17-marketing-neural-graph-v1.2.0.md)
- **[HISTORICAL_COMPLETED]** [v1.3 AI-mediated marketing plan](superpowers/plans/2026-08-17-marketing-council-v1.3-ai-mediated-marketing.md)
- **[HISTORICAL_COMPLETED]** [v1.5 Omni full-pack implementation plan](superpowers/plans/2026-09-03-omni-marketing-skill-packs.md)

Unchecked boxes inside a historical plan describe that old planning artifact. They are not current TODOs unless an ACTIVE or ONGOING document explicitly says so

## Reference material

The repository's `references/`, `neural/`, `hooks/`, and per-Skill `references/` directories are runtime/reference content rather than lifecycle-managed project documentation. Their authority is defined by the current Skills and validators

## Status vocabulary

- `ACTIVE` - current documentation
- `ONGOING` - intentionally unfinished work with explicit next verification
- `HISTORICAL_COMPLETED` - completed implementation/design record retained for history
- `HISTORICAL_SUPERSEDED` - historical record containing assumptions replaced by newer architecture
- `REFERENCE` - evergreen guidance that is useful but not itself a product contract
- `DEPRECATED` - documentation for an intentionally retired capability

The machine-readable lifecycle registry is [`document-registry.json`](document-registry.json)
