# Marketing Council for ChatGPT and Codex

Marketing Council ships as a skills-only OpenAI plugin with 29 Agent Skills, per-skill `agents/openai.yaml` metadata, shared specialist role files, references, marketing challenge gates, scripts, and brand assets.

## Repository marketplace

Add the GitHub repository as a marketplace source:

```bash
codex plugin marketplace add imMamdouhaboammar/marketing-council-pack
```

Inspect or refresh it:

```bash
codex plugin marketplace list
codex plugin marketplace upgrade marketing-council
```

Then use the ChatGPT desktop Plugins Directory to install the Marketing Council plugin from that marketplace.

The repository entry point is `.codex-plugin/plugin.json`. The repo marketplace is `.agents/plugins/marketplace.json`.

## Skills CLI alternative

To install the underlying skills directly into Codex:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a codex -y
```

This path installs the skills rather than the complete plugin wrapper.

## Package

```bash
python scripts/build_host_packages.py
```

Use `dist/release/marketing-council-openai-plugin-v1.3.0.zip` for a standalone plugin package.

## Architecture note

OpenAI plugins expose Agent Skills as native reusable components. Marketing Council's 24 specialist roles stay bundled as shared role documents selected by the main Council skill. No fake MCP dependency or executable lifecycle hook is added merely for packaging.
