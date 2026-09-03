# OpenAI / ChatGPT Plugin Release Runbook

Marketing Council is a skills-only plugin. Its public ChatGPT/Codex release must be treated as a versioned package, not as a live mirror of the GitHub repository.

## Why this exists

The public plugin submission flow captures submitted skill content as release content. Updating GitHub does not, by itself, guarantee that an already published ChatGPT plugin receives newer skill files. A changed public package must therefore use a new plugin manifest version and be resubmitted through the plugin submission flow.

This repository previously had release drift: the latest commit described a newer release while public manifests and packaging still declared `1.3.0`. That makes it possible to have newer source files in GitHub while the public plugin continues to expose an older snapshot.

## Standalone full-skill bundles

Every one of the 29 skills must also be buildable as a standalone bundle. A submitted skill cannot depend on repository-relative paths that only work when the entire GitHub checkout is present.

`scripts/build_openai_submission_pack.py` creates reviewer-ready standalone ZIPs for all 29 skills. For each skill it copies the shared agents, hooks, references, routing data, neural graph, workflows, tools, and deterministic scripts it can reference, then rewrites external repository-relative paths into bundle-local `shared/` paths.

The `marketing-council` standalone bundle additionally contains all 28 focused skill modules. Their resource references are rewritten for their nested location, so loading a focused module from the Council bundle still resolves the shared agents, hooks, references, routers, and scripts packaged with that bundle.

The submission inventory records the archive path, SHA-256 digest, size, and standalone status for each skill. This is the artifact to inspect when ChatGPT renders only part of the pack or when one skill behaves differently from the repository copy.

## Release invariants

Before every OpenAI plugin submission:

1. `.codex-plugin/plugin.json`, `manifest.json`, `submission/listing.json`, and host release metadata must declare the same release version.
2. `skills/` must contain exactly 29 `SKILL.md` files.
3. Every skill must include `agents/openai.yaml` with:
   - `interface.display_name`
   - `interface.short_description`
   - `interface.default_prompt` that names `$<skill-slug>`
   - `policy.allow_implicit_invocation: true`
4. `routing/skill-routes.json` must cover every focused skill exactly once and use `marketing-council` as fallback.
5. `scripts/skill_router.py` must route narrow requests to one focused skill and ambiguous or cross-functional requests to the council.
6. The built OpenAI plugin ZIP must contain all 29 skills, the routing registry, the router scripts, and the OpenAI plugin manifest.
7. The OpenAI submission pack must contain exactly 29 standalone skill ZIPs and no unresolved external repository references in each root `SKILL.md`.
8. The `marketing-council` standalone ZIP must include all 28 focused modules with bundle-local shared-resource paths.
9. A rebuild must remove stale generated plugin and skill archives before writing the new submission pack.
10. A public update must use a different manifest `version` from the currently published plugin version.

## Preflight

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_distribution.py . --json
python scripts/build_host_packages.py --output-root dist/release
python scripts/build_openai_submission_pack.py --output-root dist/openai-submission --json
```

Validate the exact OpenAI plugin archive for the version declared in `.codex-plugin/plugin.json`, using a fresh extraction directory on every run:

```bash
python - <<'PY'
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

root = pathlib.Path('.').resolve()
version = json.loads(
    (root / '.codex-plugin' / 'plugin.json').read_text(encoding='utf-8')
)['version']
archive = root / 'dist' / 'release' / f'marketing-council-openai-plugin-v{version}.zip'
if not archive.is_file():
    raise SystemExit(f'missing current release archive: {archive}')

with tempfile.TemporaryDirectory() as td:
    out = pathlib.Path(td)
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(out)
    subprocess.run(
        [sys.executable, str(root / 'scripts' / 'validate_openai_plugin.py'), str(out), '--json'],
        check=True,
    )
PY
```

Inspect `dist/openai-submission/submission-inventory.json` and verify `skill_count` is 29, every skill entry reports `standalone: true`, and there are exactly 29 skill ZIPs in `dist/openai-submission/skills/`.

Do not submit when any command fails.

## Submission checklist

1. Build the plugin ZIP and all standalone skill ZIPs from the exact commit being released.
2. Confirm the plugin manifest version is newer than the currently published version.
3. Confirm `submission-inventory.json` lists all 29 skills and record the hashes for the submitted artifacts.
4. Open the OpenAI plugin submission flow and update the existing Marketing Council plugin rather than creating a different plugin identity.
5. Upload the fresh plugin package and the corresponding standalone skill bundles required by the submission flow.
6. Confirm the submission preview lists all 29 skills with the expected display names and descriptions. A partial preview is a release blocker.
7. Confirm starter prompts and listing metadata match `submission/listing.json`.
8. Submit the new plugin version for review/publication.
9. After publication, install or refresh the plugin in a new ChatGPT conversation and test explicit plus implicit invocation.

## Post-publication smoke tests

Use a new chat for each class of test so stale session state does not hide discovery problems.

### Explicit focused skill

```text
@Marketing Council use pricing-strategy to build pricing tiers and discount guardrails from willingness-to-pay evidence
```

Expected: the plugin is available and the pricing skill is selected directly.

### Implicit focused routing

```text
Build a pricing strategy with willingness to pay, price architecture, and discount guardrails
```

Expected: `pricing-strategy` owns the request without running the full council.

### Single explicit intent

```text
Reduce churn
```

Expected: `retention-strategy` owns the request rather than unnecessarily loading the full council.

### Negative-route boundary

```text
Write brand copy without competitor research
```

Expected: the request must not be routed to `competitive-intelligence` merely because it contains the phrase `competitor research`.

### Cross-functional fallback

```text
Create the full go-to-market strategy including positioning, pricing, campaign, media, retention, and measurement
```

Expected: `marketing-council` remains the primary skill and dispatches multiple focused skills.

### Newer skill coverage

```text
Design a geo holdout test to estimate incremental ROAS and reconcile it with attribution
```

Expected: `incrementality-design` is discoverable and callable.

### Previously inconsistent metadata coverage

Smoke-test at least one of these skills because their OpenAI metadata previously omitted implicit invocation policy:

`brand-strategy`, `product-marketing`, `segmentation-strategy`, `category-strategy`, `behavioral-marketing`, `marketing-measurement`

## Failure triage

If GitHub contains a skill but ChatGPT does not show or invoke it, check in this order:

1. Was the public plugin actually resubmitted after the skill was added or changed?
2. Did the manifest `version` change?
3. Does `submission-inventory.json` contain exactly 29 current skill archives and no stale artifacts?
4. Does the submitted standalone ZIP contain its root `SKILL.md`, `agents/openai.yaml`, and every referenced support file?
5. For `marketing-council`, does the standalone bundle contain all 28 focused modules and their rewritten shared-resource paths?
6. Does the submission preview list all 29 skills before publication?
7. Does the skill description distinguish its intent from sibling skills?
8. Is implicit invocation enabled in `agents/openai.yaml`?
9. Does explicit `$skill-name` invocation work while implicit routing fails? If yes, treat it as a routing or discovery-metadata problem rather than a packaging problem.
10. Does the plugin itself fail to resolve in the public directory? If yes, investigate release/listing state before changing skill prompts.

## Source versus public release

The GitHub marketplace and the universal public plugin directory are separate distribution surfaces. A repository can be internally correct while the public plugin still exposes an older submitted release. Release verification therefore has to validate both the source package and the published ChatGPT behavior.

Use these release states precisely:

`source-valid`, `package-valid`, `submission-ready`, `submitted`, `approved`, `published`

A green repository CI run can establish the first two and support `submission-ready`. It does not prove that the public ChatGPT directory has been updated.
