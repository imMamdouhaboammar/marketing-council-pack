# Marketing Council for Claude Code

The Claude plugin exposes all 29 Agent Skills plus all 24 specialist roles as native Claude plugin resources. The skill inventory is 28 focused skills plus the `marketing-council` router and cross-functional fallback.

## Install from the marketplace

Inside Claude Code:

```text
/plugin marketplace add imMamdouhaboammar/marketing-council-pack
/plugin install marketing-council@marketing-council
```

Plugin skills are namespaced by Claude under `marketing-council:*`. Specialist agents are loaded from the plugin's `agents/` directory.

## Skills CLI alternative

Install the 29 Agent Skills only:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a claude-code -y
```

The Skills CLI route does not install the native Claude subagents. Use the marketplace route when you want the full Council package.

## Validate

```bash
claude plugin validate . --strict
```

## Package

```bash
python scripts/build_host_packages.py --output-root dist/release
```

The generated `dist/release/marketing-council-claude-marketplace-v1.5.0.zip` is the self-contained v1.5.0 local marketplace. Its marketplace entry points to `./plugins/marketing-council`, so the extracted package does not depend on files outside the release artifact.
