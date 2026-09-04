# Marketing Council for ChatGPT and Codex

Marketing Council ships as a skills-only OpenAI plugin with 29 Agent Skills: 28 focused skills plus the `marketing-council` router and cross-functional fallback. Each public skill has `agents/openai.yaml` metadata, and the source repository also includes shared specialist roles, references, challenge gates, routers, deterministic scripts, and brand assets.

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

Then install Marketing Council from the supported plugin directory surface.

The repository entry point is `.codex-plugin/plugin.json`. The repo marketplace is `.agents/plugins/marketplace.json`.

## Skills CLI alternative

To install the underlying 29 Agent Skills directly into Codex:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a codex -y
```

This path installs the skills rather than the complete plugin wrapper.

## Package

```bash
python scripts/build_host_packages.py --output-root dist/release
```

Use `dist/release/marketing-council-openai-plugin-v1.5.0.zip` for the v1.5.0 standalone plugin package.

For public OpenAI submission, also build the per-skill submission artifacts:

```bash
python scripts/build_openai_submission_pack.py --output-root dist/openai-submission --json
```

That output must contain 29 standalone skill bundles. Updating GitHub alone does not replace an already published public skill snapshot. Follow `docs/OPENAI_RELEASE.md` for resubmission and post-publication smoke tests.

## Architecture note

The focused skill router and the neural/theory router are separate. The first chooses the owning skill; the second ranks marketing lenses after diagnosis. The 24 specialist roles remain shared decision resources selected by the Council. No artificial MCP dependency or executable lifecycle hook is added solely for packaging.
