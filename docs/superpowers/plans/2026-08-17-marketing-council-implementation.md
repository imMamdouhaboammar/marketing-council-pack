<!--
doc_status: HISTORICAL_COMPLETED
created: 2026-08-17
last_reviewed: 2026-09-04
completed_by_release: v1.0.0
source_of_truth: false
-->

![Status: HISTORICAL_COMPLETED](https://img.shields.io/badge/status-historical__completed-6b7280)

> [!NOTE]
> **Historical implementation plan**
>
> Status: `HISTORICAL_COMPLETED`
>
> Completed by release: `v1.0.0`
>
> This file preserves the implementation sequence used for the initial Marketing Council release. It is not the current product contract or backlog
>
> **Current source of truth:**
> - [Repository README](../../../README.md)
> - [Documentation map](../../README.md)
> - [OpenAI release runbook](../../OPENAI_RELEASE.md)
>
> Do not execute this plan as a current task list

# Marketing Council Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Build a validated, portable Marketing Council agent-skill pack with orchestrated expert roles, decision skills, hooks, deterministic scripts, host adapters, and behavioral evals.

**Architecture:** Keep one host-neutral core based on the Agent Skills `SKILL.md` format. Domain skills, agents, hooks, workflows, and references are plain Markdown; deterministic calculations and linting are Python; host adapters explain installation/discovery without duplicating the marketing logic.

**Tech Stack:** Markdown, YAML/JSON, Python 3 standard library, unittest, shell-compatible install helpers.

## Global Constraints

- Never role-play or imitate living/dead marketers; encode decision principles and source attribution instead.
- Main SKILL.md files must use valid lowercase hyphenated names and stay concise for progressive disclosure.
- Time-sensitive claims must trigger fresh research when network/search is available.
- Strategy must distinguish evidence from assumptions and must include measurable thresholds.
- Core files must not hard-code one AI host's tool names.
- Python scripts must use only the standard library.
- All executable scripts require tests.
- Package must include generic, Claude, Codex/OpenAI, and GitHub Copilot adapter guidance.

---

### Task 1: Core pack and orchestration

**Files:**
- Create: `README.md`, `LICENSE`, `skills/marketing-council/SKILL.md`
- Create: `agents/*.md`
- Test: `tests/test_pack_structure.py`

**Interfaces:**
- Produces: portable main skill, role contracts, output schemas, routing rules.

- [x] Write structure/frontmatter tests first and verify they fail.
- [x] Create the main skill and 12 role files.
- [x] Re-run structure tests and make them pass.
- [x] Commit the task.

### Task 2: Domain skills, hooks, and workflows

**Files:**
- Create: `skills/*/SKILL.md` for diagnosis, research, positioning, audience, offer, pricing, go-to-market, campaign, media, content, CRO, retention, experimentation.
- Create: `hooks/*.md`, `workflows/*.md`
- Test: extend `tests/test_pack_structure.py`

**Interfaces:**
- Consumes: main routing contract from Task 1.
- Produces: focused callable skills and guardrails.

- [x] Add failing discovery/reference tests.
- [x] Implement domain skills, hooks, and workflows.
- [x] Run tests to green.
- [x] Commit the task.

### Task 3: Marketing knowledge canon and decision rules

**Files:**
- Create: `references/canon/*.md`, `references/decision-rules/*.md`, `references/frameworks/*.md`, `references/sources.yml`
- Test: `tests/test_reference_integrity.py`

**Interfaces:**
- Produces: concise source-attributed principle cards with applicability, misuse, counterweights, and questions.

- [x] Add failing integrity tests requiring principle structure and source keys.
- [x] Implement the reference library without copyrighted long-form excerpts.
- [x] Run tests to green.
- [x] Commit the task.

### Task 4: Deterministic marketing utilities

**Files:**
- Create: `scripts/unit_economics.py`, `scripts/funnel_math.py`, `scripts/experiment_math.py`, `scripts/tactic_ranker.py`, `scripts/strategy_linter.py`, `scripts/validate_pack.py`
- Test: `tests/test_scripts.py`

**Interfaces:**
- Produces: CLI-safe JSON outputs and pure functions for calculation, ranking, linting, and pack validation.

- [x] Write behavior tests and verify they fail because modules do not exist.
- [x] Implement minimal utilities with explicit validation errors.
- [x] Run all script tests to green.
- [x] Commit the task.

### Task 5: Host adapters and installation helpers

**Files:**
- Create: `adapters/generic/README.md`, `adapters/claude/README.md`, `adapters/openai/README.md`, `adapters/copilot/README.md`
- Create: `install.sh`, `install.ps1`, `manifest.json`
- Test: `tests/test_adapters.py`

**Interfaces:**
- Produces: documented install destinations and a generic manifest without changing core behavior.

- [x] Add failing adapter/manifest tests.
- [x] Implement adapter docs and safe install helpers.
- [x] Run tests to green.
- [x] Commit the task.

### Task 6: Eval suite, examples, and release package

**Files:**
- Create: `evals/cases/*.yml`, `evals/adversarial/*.yml`, `evals/RUBRIC.md`, `examples/*.md`, `CHANGELOG.md`
- Test: `tests/test_evals.py`

**Interfaces:**
- Produces: scenario-based behavioral evaluation set and human-readable examples.

- [x] Add failing eval-schema tests.
- [x] Implement at least eight core cases and five adversarial cases.
- [x] Run the entire test suite and pack validator.
- [x] Produce a zip archive.
- [x] Commit the task.
