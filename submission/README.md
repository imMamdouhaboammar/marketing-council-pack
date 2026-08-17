# Submission and release pack

This folder contains human-readable listing copy. Native host manifests live at:

```text
.codex-plugin/plugin.json
.agents/plugins/marketplace.json
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

Build deterministic release artifacts with:

```bash
python scripts/build_host_packages.py
```

Validate source distribution metadata with:

```bash
python scripts/validate_distribution.py --json
```

The generated OpenAI package is skills-only. The generated Claude marketplace contains all 29 skills and 24 native specialist agents. The single-skill package is a self-contained portable build produced from the same source.
