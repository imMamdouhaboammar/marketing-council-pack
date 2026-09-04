<!--
doc_status: ONGOING
last_reviewed: 2026-09-04
release: 1.5.0
source_of_truth: false
-->

![Status: ONGOING](https://img.shields.io/badge/status-ONGOING-2563eb)
![Release: v1.5.0](https://img.shields.io/badge/release-v1.5.0-173F35)

## Operational status

- **Status:** `ONGOING`
- **Current state:** source and package artifacts are validated locally/CI; the repository submission draft intentionally remains `PARTIAL_MISSING_INPUT`
- **Completed work:** 29 standalone Skill bundles, plugin package validation, five positive and three negative evidence-bound cases, release notes, and deterministic submission-draft validation
- **Remaining work:** supply verified publisher identity, Privacy Policy URL, Terms URL, Support URL, and country/region availability; then complete portal scan/review, submit, publish after approval, and run fresh ChatGPT/Codex smoke tests
- **Blockers:** required external portal inputs are not stored in the repository and must not be invented
- **Next verification step:** resolve all `missing_required_inputs` in `submission/submission-pack.json`, rebuild from the exact release commit, then follow `docs/OPENAI_RELEASE.md`
- **Source-of-truth references:** `submission/submission-pack.json`, `docs/OPENAI_RELEASE.md`, current manifests, builders, and package validators
- **Last reviewed date:** 2026-09-04

# Submission and release pack

Marketing Council v1.5.0 is packaged as a **skills-only** OpenAI plugin with 29 total Skills: 28 focused Skills plus the `marketing-council` router and fallback

## Current submission state

The repository-owned submission draft is:

```text
submission/submission-pack.json
```

Its status is intentionally `PARTIAL_MISSING_INPUT`, not `submission-ready`

The draft contains exactly five positive and three negative reviewer cases backed by executed v1.5.0 router or Dynamic DAG regression tests. It also records the release boundary explicitly: portal scan, policy attestation, submission, approval, publication, and public ChatGPT/Codex verification have not been performed

The remaining external inputs are:

- verified developer identity in the submission portal
- privacy policy URL
- terms of service URL
- support URL
- country or region availability

Do not invent or infer those values from repository metadata

Validate the evidence-bound draft with:

```bash
python scripts/validate_submission_pack.py submission/submission-pack.json --json
```

## Native host manifests

```text
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

## Build and validate

Build deterministic host release artifacts with:

```bash
python scripts/build_host_packages.py --output-root dist/release
```

Build the 29 standalone OpenAI Skill bundles with:

```bash
python scripts/build_openai_submission_pack.py --output-root dist/openai-submission --json
```

Validate source distribution metadata with:

```bash
python scripts/validate_distribution.py . --json
```

The release builders reject symlink sources before copying or archiving them. The OpenAI package is skills-only. The Claude marketplace contains all 29 Skills and 24 native specialist agents. The portable Council package is a self-contained build produced from the same source
