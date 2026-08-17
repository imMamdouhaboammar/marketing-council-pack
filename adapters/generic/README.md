# Marketing Council for Agent Skills hosts

Marketing Council uses portable `SKILL.md` files as its primary distribution surface.

Install all 29 skills across every agent supported by the Skills CLI:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --all -y
```

List available skills first:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --list
```

For a host not covered by the CLI, build the self-contained main skill:

```bash
python scripts/build_dist.py
```

Copy `dist/marketing-council/` into that host's Agent Skills directory. The built skill contains the shared roles, challenge gates, references, workflows, scripts, tool contracts, and focused skill modules it needs.

The portable build also includes `neural/graph.json`, figure/school/theory references, and the deterministic neural router.
