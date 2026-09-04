<!--
doc_status: HISTORICAL_COMPLETED
created: 2026-08-17
last_reviewed: 2026-09-04
completed_by_release: v1.1.0
source_of_truth: false
-->

![Status: HISTORICAL_COMPLETED](https://img.shields.io/badge/status-historical__completed-6b7280)

> [!NOTE]
> **Historical implementation plan**
>
> Status: `HISTORICAL_COMPLETED`
>
> Completed by release: `v1.1.0`
>
> This file preserves the original distribution work plan. Its unchecked boxes are historical planning state, not current repository TODOs
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> Do not execute this plan as a current task list

# Marketing Council Distribution v1.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship Marketing Council as a polished GitHub product with native ChatGPT/Codex plugin packaging, a Claude Code marketplace/plugin, accurate `npx skills` install commands, and a marketing-first README.

**Architecture:** Keep `skills/`, `agents/`, references, scripts, and workflows as the single source of truth. Add host-native manifests at the repository root, enrich each portable skill with OpenAI UI metadata, make every role file a valid Claude plugin subagent, and build clean host-specific release archives from the same source tree.

**Tech Stack:** Markdown, JSON, YAML, Python 3.10+, unittest, Agent Skills, OpenAI plugins, Claude Code plugins/marketplaces, Vercel `skills` CLI.

## Global Constraints

- Repository identity: `imMamdouhaboammar/marketing-council-pack`.
- Release version: `1.1.0`.
- OpenAI plugin architecture: skills-only. No MCP server is invented.
- Claude plugin must expose all 14 skills and all 12 specialist agents.
- OpenAI plugin must expose all 14 skills and bundle all shared agent role documents used by the council.
- `npx skills` documentation must use commands supported by the current `vercel-labs/skills` CLI.
- README copy must distinguish strategy from tactics, avoid celebrity impersonation, and avoid generic marketing claims.
- Public package manifests must point only to files inside the package and must not contain secrets or executable lifecycle hooks.

---

### Task 1: Distribution contract tests

**Files:**
- Create: `tests/test_distribution.py`

**Interfaces:**
- Consumes: existing `skills/`, `agents/`, `manifest.json`.
- Produces: failing contract tests for OpenAI manifest, Claude marketplace/plugin, OpenAI skill metadata, Claude agent frontmatter, README install commands, and release packaging.

- [ ] Write tests that require `.codex-plugin/plugin.json`, `.agents/plugins/marketplace.json`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, 14 `agents/openai.yaml` files, 12 valid Claude agents, and version `1.1.0`.
- [ ] Run `python -m unittest tests.test_distribution -v` and confirm it fails because the new distribution files are absent.
- [ ] Commit the red test contract.

### Task 2: Native host manifests and metadata

**Files:**
- Create: `.codex-plugin/plugin.json`
- Create: `.agents/plugins/marketplace.json`
- Create: `.claude-plugin/plugin.json`
- Create: `.claude-plugin/marketplace.json`
- Create: `assets/logo.svg`
- Create: `assets/composer-icon.svg`
- Create: `skills/*/agents/openai.yaml`
- Modify: `agents/*.md`
- Modify: `manifest.json`
- Modify: `skills/*/SKILL.md`

**Interfaces:**
- Produces valid host discovery metadata while keeping skill logic unchanged.

- [ ] Add the OpenAI skills-only plugin manifest with `skills: ./skills/` and current directory metadata.
- [ ] Add the OpenAI repo marketplace pointing to the Git repository.
- [ ] Add the Claude plugin manifest with `skills: ./skills/` and `agents: ./agents/`.
- [ ] Add the Claude marketplace entry for the same Git repository.
- [ ] Add square SVG branding assets.
- [ ] Add concise `agents/openai.yaml` metadata to all 14 skills.
- [ ] Add `name` and trigger-focused `description` frontmatter to all 12 Claude agent files.
- [ ] Bump package and skill metadata to `1.1.0`.
- [ ] Run `python -m unittest tests.test_distribution -v` and make the manifest/metadata tests pass.

### Task 3: Host packaging and validation

**Files:**
- Create: `scripts/build_host_packages.py`
- Create: `scripts/validate_distribution.py`
- Modify: `tests/test_distribution.py`

**Interfaces:**
- `build_host_packages(output_root: Path) -> dict[str, Path]`
- `validate_distribution(root: Path) -> dict`

- [ ] Add tests for clean OpenAI plugin and Claude marketplace archive roots.
- [ ] Implement deterministic host package copying and ZIP creation without `.git`, tests, caches, or local docs.
- [ ] Implement structural validation for manifest paths, component counts, version alignment, agent frontmatter, and marketplace source identity.
- [ ] Run the new distribution tests and existing full suite.

### Task 4: Marketing README and install documentation

**Files:**
- Modify: `README.md`
- Modify: `adapters/openai/README.md`
- Modify: `adapters/claude/README.md`
- Modify: `CHANGELOG.md`
- Modify: `submission/listing.json`

**Interfaces:**
- README must contain verified `npx skills`, Codex marketplace, ChatGPT/Codex plugin, and Claude marketplace commands.

- [ ] Rewrite README around the product problem, the council model, evidence/commercial gates, examples, and installation paths.
- [ ] Document `npx skills add ... --all`, targeted Codex/Claude installs, list/use/update commands, and clarify that `npx skills` installs skills rather than Claude plugin subagents.
- [ ] Document Claude marketplace add/install/validate commands.
- [ ] Document Codex marketplace add/list/upgrade commands and ChatGPT plugin package use.
- [ ] Update listing copy and changelog for `1.1.0`.

### Task 5: Release gate

**Files:**
- Generated: `dist/marketing-council-openai-plugin-v1.1.0.zip`
- Generated: `dist/marketing-council-claude-marketplace-v1.1.0.zip`
- Generated: `dist/marketing-council-skill-v1.1.0.zip`

**Interfaces:**
- All generated archives must validate after extraction and have SHA256 hashes.

- [ ] Run `python -m unittest discover -s tests -v`.
- [ ] Run `python scripts/validate_pack.py`.
- [ ] Run `python scripts/validate_distribution.py`.
- [ ] Run `python scripts/build_host_packages.py` twice and compare SHA256 hashes.
- [ ] Extract each archive and re-run relevant structural validation.
- [ ] Record hashes in `dist/SHA256SUMS.txt` and commit the release source tree.
