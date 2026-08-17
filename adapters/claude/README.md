# Marketing Council for Claude Code

The Claude plugin exposes all 20 Marketing Council skills plus all 24 specialist roles as native Claude subagents.

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

The Skills CLI route does not install the native Claude subagents. Use the marketplace route when you want the full Council.

## Validate

```bash
claude plugin validate . --strict
```

## Package

```bash
python scripts/build_host_packages.py
```

The generated `dist/release/marketing-council-claude-marketplace-v1.3.0.zip` is a self-contained local marketplace. Its marketplace entry points to `./plugins/marketing-council`, so the plugin can be installed from the extracted package without reaching outside that package for its component files.
