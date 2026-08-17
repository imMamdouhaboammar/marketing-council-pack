# Marketing Council for GitHub Copilot

Marketing Council is portable through the Agent Skills layout. The simplest cross-host path is the Skills CLI:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --list
```

Then choose the Copilot target exposed by your installed Skills CLI version, or install to all supported agents:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --all -y
```

The repository keeps its marketing logic host-neutral. Host-specific tool access is bound through `tools/capabilities.yml` rather than hard-coded into the skills.
