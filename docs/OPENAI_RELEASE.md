# OpenAI / ChatGPT Plugin Release Runbook

Marketing Council is a skills-only plugin. Its public ChatGPT/Codex release must be treated as a versioned package, not as a live mirror of the GitHub repository.

## Why this exists

The public plugin submission flow captures the submitted skill bundle as release content. Updating GitHub does not, by itself, guarantee that an already published ChatGPT plugin receives the new skill files. A changed public package must therefore use a new plugin manifest version and be resubmitted through the plugin submission flow.

This repository previously had release drift: the latest commit described a newer release while public manifests and packaging still declared `1.3.0`. That makes it possible to have newer source files in GitHub while the public plugin continues to expose an older snapshot.

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
6. The built OpenAI ZIP must contain all 29 skills and the OpenAI plugin manifest.
7. A public update must use a different manifest `version` from the currently published plugin version.

## Preflight

Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate_distribution.py . --json
python scripts/build_host_packages.py --output-root dist/release
```

Extract the generated OpenAI package and validate it:

```bash
mkdir -p /tmp/marketing-council-openai
python - <<'PY'
import pathlib, zipfile
root = pathlib.Path('dist/release')
archive = next(root.glob('marketing-council-openai-plugin-v*.zip'))
out = pathlib.Path('/tmp/marketing-council-openai')
with zipfile.ZipFile(archive) as zf:
    zf.extractall(out)
print(archive)
PY
python scripts/validate_openai_plugin.py /tmp/marketing-council-openai --json
```

Do not submit when any command fails.

## Submission checklist

1. Build a fresh skills-only ZIP from the exact commit being released.
2. Confirm the ZIP manifest version is newer than the currently published version.
3. Open the OpenAI plugin submission flow and update the existing Marketing Council plugin rather than creating a different plugin identity.
4. Upload the fresh ZIP.
5. Confirm the submission preview lists all 29 skills.
6. Confirm starter prompts and listing metadata match `submission/listing.json`.
7. Submit the new plugin version for review/publication.
8. After publication, install or refresh the plugin in a new ChatGPT conversation and test explicit plus implicit invocation.

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

Expected: pricing-strategy owns the request without running the full council.

### Cross-functional fallback

```text
Create the full go-to-market strategy including positioning, pricing, campaign, media, retention, and measurement
```

Expected: Marketing Council remains the primary skill and dispatches multiple focused skills.

### Newer skill coverage

Test at least one skill added in the latest capability layer, for example:

```text
Design a geo holdout test to estimate incremental ROAS and reconcile it with attribution
```

Expected: incrementality-design is discoverable and callable.

## Failure triage

If GitHub contains a skill but ChatGPT does not show or invoke it, check in this order:

1. Was the public plugin actually resubmitted after the skill was added?
2. Did the manifest `version` change?
3. Does the uploaded ZIP contain the skill folder and `agents/openai.yaml`?
4. Does the skill description distinguish its intent from sibling skills?
5. Is implicit invocation enabled in `agents/openai.yaml`?
6. Does explicit `$skill-name` invocation work while implicit routing fails? If yes, treat it as a routing/discovery-metadata problem rather than a packaging problem.
7. Does the plugin itself fail to resolve in the public directory? If yes, investigate release/listing state before changing skill prompts.

## Source versus public release

The GitHub marketplace and the universal public plugin directory are separate distribution surfaces. A repository can be internally correct while the public plugin still exposes an older submitted release. Release verification therefore has to validate both the source package and the published ChatGPT behavior.
