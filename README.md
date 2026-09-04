<div align="center">

<img src="assets/logo.svg" alt="Marketing Council" width="108" height="108" />

# Marketing Council

### Make the model diagnose, route, challenge, and defend the marketing decision before it writes tactics

**29 Agent Skills. 28 focused skills + 1 Council router. 24 specialist agents. 25 marketing figures. 46 applied theories.**

[![Version](https://img.shields.io/badge/version-1.5.0-173F35)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-29-173F35)](skills/)
[![Specialist Agents](https://img.shields.io/badge/Specialist%20Agents-24-173F35)](agents/)
[![License](https://img.shields.io/badge/license-MIT-173F35)](LICENSE)

</div>

Marketing Council is a cross-agent marketing strategy plugin for ChatGPT, Codex, Claude Code, and compatible Agent Skills hosts

It uses three routing layers that should not be confused

1. The **skill router** decides which of the 28 focused marketing skills owns the request, or falls back to `marketing-council` when the brief is ambiguous or cross-functional
2. The **dynamic DAG router** builds a bounded dependency graph only when the request explicitly requires dependent work across multiple focused skills
3. The **neural router** works after skill ownership is known to rank relevant schools, theories, principles, specialist agents, and counterweights

The goal is not to produce a longer brainstorm. The goal is to make one defensible marketing decision with explicit evidence, assumptions, trade-offs, measurement, and reversal criteria

## What changed in v1.5.0

Version 1.5.0 turns every Marketing Council Skill into a fully rendered behavioral and execution pack

- all 29 Agent Skills carry local decision, evidence, failure-mode, output, and behavioral-eval artifacts
- the 28 focused Skills are mapped through `routing/skill-execution-bindings.json` to a primary specialist, skeptical counterweight, domain challenge gate, and evidence gate
- `scripts/skill_router.py` owns single-skill selection and conservative Council fallback
- `scripts/dynamic_router.py` owns bounded dependency DAGs for explicitly dependent cross-functional work, preserves explicit request order, and requires every transition to resolve through a declared handoff
- `scripts/neural_router.py` remains a separate post-ownership theory and specialist router
- Council standalone packaging embeds all 28 focused Skills and rewrites shared agent, hook, routing, neural, and tool dependencies into bundle-local resources
- self-contained, host, and standalone OpenAI builders reject symlink sources before copying or archiving release content
- `submission/submission-pack.json` carries five positive and three negative executed review cases; it remains `PARTIAL_MISSING_INPUT` until required portal identity, policy/support URLs, and availability fields are supplied
- renderer drift, execution-binding resolution, evidence-ledger coverage, structural BinEval, router regressions, host packaging, and OpenAI submission packaging are CI-gated
- public OpenAI availability still requires submitting or resubmitting the v1.5.0 snapshot and running fresh-chat smoke tests after publication

## Documentation status

Use [`docs/README.md`](docs/README.md) as the canonical documentation map. It separates ACTIVE and ONGOING operational docs from historical specs and implementation plans so old planning assumptions are not treated as current requirements

## Architecture

```text
USER REQUEST
     |
     v
SKILL ROUTER
routing/skill-routes.json
scripts/skill_router.py
     |
     +--> one dominant function --> focused Skill
     |
     +--> ambiguous ownership --> marketing-council
     |
     +--> explicit dependent cross-functional work
                    |
                    v
              DYNAMIC DAG ROUTER
              scripts/dynamic_router.py
                    |
                    v
              bounded focused-Skill DAG
                    |
                    v
              DECISION + EVIDENCE
                    |
                    v
              NEURAL ROUTER
              neural/graph.json
              scripts/neural_router.py
                    |
                    v
              theories / agents / counterweights
                    |
                    v
              CHALLENGE + DECISION

Focused Skill execution wiring:
routing/skill-execution-bindings.json
     -> primary specialist
     -> skeptical counterweight
     -> domain challenge gate
     -> evidence gate
```

### Skill router

The skill router answers a product-level question

> Which skill should own this request?

It uses `routing/skill-routes.json`, where every focused skill has

- canonical intent phrases
- positive examples
- negative examples
- priority

The router is conservative. If several functions are strongly active, it does not force the request into one narrow skill. It returns to `marketing-council`

Try it directly

```bash
python scripts/skill_router.py \
  --text "Design a geo holdout to estimate incremental ROAS" \
  --json
```

Expected primary skill

```text
incrementality-design
```

Cross-functional example

```bash
python scripts/skill_router.py \
  --text "Build positioning, pricing, media, campaign, retention, and measurement strategy" \
  --json
```

Expected primary skill

```text
marketing-council
```

### Dynamic DAG router

The dynamic router answers a dependency question

> Which focused Skills must run, and in what dependency order, when the user has explicitly established a cross-functional chain?

```bash
python scripts/dynamic_router.py --help
```

It is deliberately bounded. It does not create a DAG merely because several marketing functions are mentioned. Ambiguous ownership stays with `marketing-council`, while genuinely dependent work is limited to the minimum focused Skills required by the decision

Execution ownership inside each focused Skill is declared separately in `routing/skill-execution-bindings.json`

### Neural router

The neural router answers a different question

> Which marketing lenses, theories, agents, and counterweights are relevant after we understand the problem?

```bash
python scripts/neural_router.py \
  --signals category-mature,differentiation-weak,competitor-pressure-high \
  --json
```

The graph currently connects marketing schools, principles, applied theories, diagnostic signals, specialist agents, focused skills, challenge hooks, and dated evidence cards

Named marketing figures are source references, not role-play personas. A named figure never settles a debate by authority

## The 29 Agent Skills

`marketing-council` is the router and cross-functional fallback. The other 28 are focused skills

| Skill | Primary job |
|---|---|
| `marketing-council` | Route ambiguous or cross-functional work, arbitrate disagreements, and make the final strategic choice |
| `market-diagnosis` | Diagnose market structure, demand, and growth constraints before choosing tactics |
| `customer-research` | Design and interpret customer evidence, interviews, JTBD, switching triggers, and customer language |
| `segmentation-strategy` | Build commercially useful segmentation and targeting choices |
| `positioning-strategy` | Define competitive alternatives, category frame, differentiation, and reason to choose |
| `category-strategy` | Decide category definition, maturity, entry points, and whether reframing is justified |
| `brand-strategy` | Brand associations, memory, architecture, equity, and distinctive assets |
| `product-marketing` | Product truth, proposition, demonstration, feature story, and launch narrative |
| `offer-strategy` | Offer architecture, proof, objections, guarantees, risk reversal, and direct-response mechanics |
| `pricing-strategy` | Price architecture, willingness to pay, tiers, sensitivity, and discount guardrails |
| `go-to-market` | Market entry, route to market, launch sequence, and GTM coordination |
| `campaign-strategy` | Campaign objective, proposition, creative territory, audience action, and measurement |
| `media-strategy` | Channel roles, reach, paid distribution, allocation, and media fit |
| `content-strategy` | Editorial choices, content jobs, formats, distribution, and buying-situation relevance |
| `behavioral-marketing` | Friction, choice architecture, defaults, ethical influence, social proof, and behavior change |
| `conversion-strategy` | Funnel friction, checkout, forms, landing pages, CRO, and drop-off diagnosis |
| `retention-strategy` | Churn, lifecycle, renewal, repeat purchase, reactivation, and customer retention |
| `competitive-intelligence` | Competitors, substitutes, rivalry, pressure, and defensibility |
| `marketing-measurement` | KPI architecture, attribution, MMM, measurement plans, and uncertainty |
| `marketing-experimentation` | Hypotheses, A/B tests, experiment roadmaps, and learning plans |
| `ai-discovery-strategy` | AI search, answer surfaces, citations, retrievability, and conversational discovery |
| `conversational-advertising` | Conversational ad experiences and interactive ad decision flows |
| `agentic-commerce` | Agent-mediated shopping, product truth, machine buyers, and agent checkout readiness |
| `commerce-feed-intelligence` | Product, merchant, catalog, and structured commerce feed quality |
| `autonomous-media-operations` | AI-assisted media authority, guardrails, rollback, and operational control |
| `marketing-signal-strategy` | CRM, value, offline conversion, optimization, and signal-quality strategy |
| `incrementality-design` | Holdouts, geo tests, counterfactuals, incremental CAC/ROAS, and causal lift |
| `creator-commerce` | Creator discovery, media, affiliate, search, commerce, and creator measurement |
| `commerce-media-strategy` | Retail media, marketplace ads, shopper media, and closed-loop measurement bias |

## The Council

The repository contains 24 specialist role definitions under `agents/`

Representative roles include

- `market-architect`
- `audience-strategist`
- `positioning-strategist`
- `product-marketing-director`
- `response-strategist`
- `behavior-strategist`
- `brand-growth-strategist`
- `commercial-strategist`
- `channel-strategist`
- `measurement-strategist`
- `creative-strategist`
- `competitive-strategy-analyst`
- `ai-discovery-strategist`
- `agentic-commerce-strategist`
- `marketing-automation-governor`
- `marketing-signal-architect`
- `creator-commerce-strategist`
- `commerce-media-strategist`
- `marketing-skeptic`
- `council-director`

The Council should run only roles that can materially change the decision. A narrow task should not automatically load the entire council

## Decision discipline

Marketing Council separates load-bearing statements into explicit evidence states when uncertainty matters

```text
FACT
EVIDENCE
INFERENCE
ASSUMPTION
HYPOTHESIS
UNKNOWN
```

A recommendation should be revised if it

- invents customer psychology or market facts
- treats platform attribution as causal proof
- chooses a channel because it is popular rather than suitable
- ignores margin, capacity, retention, or payback when they matter
- produces a long tactic list without a primary strategic choice
- hides meaningful uncertainty
- could be sent unchanged to several unrelated businesses

## Install

### Skills CLI

Install all 29 skills across supported agents

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --all -y
```

List available skills first

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --list
```

Install all skills for Codex

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a codex -y
```

Install all skills for Claude Code

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a claude-code -y
```

Install only the Council skill

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill marketing-council -g -y
```

### ChatGPT and Codex plugin marketplace

```bash
codex plugin marketplace add imMamdouhaboammar/marketing-council-pack
```

Then inspect or refresh the marketplace

```bash
codex plugin marketplace list
codex plugin marketplace upgrade marketing-council
```

### Claude Code marketplace

```text
/plugin marketplace add imMamdouhaboammar/marketing-council-pack
/plugin install marketing-council@marketing-council
```

## OpenAI plugin package

Build host packages

```bash
python scripts/build_host_packages.py --output-root dist/release
```

The OpenAI plugin archive for this release is

```text
dist/release/marketing-council-openai-plugin-v1.5.0.zip
```

The repository also builds a Claude marketplace package and a self-contained Agent Skill package for the same version

## OpenAI submission pack

A valid repository ZIP is not enough to prove a public ChatGPT release contains every skill

OpenAI skills are versioned bundles. Marketing Council source skills share agents, hooks, references, routing data, the neural graph, workflows, tools, and deterministic scripts. For public submission, those dependencies must travel with the submitted skill rather than relying on the GitHub checkout existing at runtime

Build the submission pack

```bash
python scripts/build_openai_submission_pack.py \
  --output-root dist/openai-submission \
  --json
```

Expected output includes

```text
dist/openai-submission/submission-inventory.json
dist/openai-submission/skills/market-diagnosis-v1.5.0.zip
...
dist/openai-submission/skills/marketing-council-v1.5.0.zip
```

The inventory must report exactly 29 standalone skill bundles and includes SHA-256 hashes for the artifacts

Generated standalone skills rewrite source references such as

```text
../../agents/...
../../hooks/...
../../references/...
```

into bundle-local paths under

```text
shared/agents/...
shared/hooks/...
shared/references/...
```

A generated `SKILL.md` with an unresolved `../../` dependency is a release blocker

## Public ChatGPT release rule

Updating GitHub does not update an already published ChatGPT plugin release by itself

After public skill content changes

1. increment the plugin version
2. run the complete release gates
3. build the plugin package and the 29 standalone skill bundles
4. update the existing Marketing Council submission in the OpenAI plugin submission flow
5. confirm the submission preview lists all 29 skills
6. submit the new version
7. after publication, test explicit invocation, implicit focused routing, cross-functional fallback, and newer skill coverage in fresh chats

See [`docs/OPENAI_RELEASE.md`](docs/OPENAI_RELEASE.md) for exact smoke tests and failure triage

## Validate

Run the full suite

```bash
python -m unittest discover -s tests -v
```

Validate source distribution

```bash
python scripts/validate_distribution.py . --json
```

Build packages

```bash
python scripts/build_host_packages.py --output-root dist/release
```

Build standalone submission skills

```bash
python scripts/build_openai_submission_pack.py --output-root dist/openai-submission --json
```

Validate an extracted OpenAI plugin package

```bash
python scripts/validate_openai_plugin.py /path/to/extracted-plugin --json
```

CI runs the same release-critical checks for pull requests to `main` and pushes to `main`

## Repository structure

```text
.codex-plugin/             OpenAI / ChatGPT / Codex plugin manifest
.claude-plugin/            Claude plugin and marketplace metadata
.agents/plugins/           repository marketplace metadata
skills/                    29 Agent Skills
agents/                    24 specialist role definitions
routing/                   focused skill route registry
neural/                    marketing graph and signals
hooks/                     challenge and decision gates
references/                canon, figures, theory, and dated evidence cards
workflows/                 end-to-end workflow guidance
scripts/                   routers, calculations, builders, and validators
tools/                     host capability contracts
evals/                     business and adversarial evaluation cases
submission/                public listing metadata
docs/OPENAI_RELEASE.md     OpenAI release and resubmission runbook
```

## Current evidence and marketing theory

Timeless marketing principles and changing platform facts are intentionally separated

Current-state evidence for AI discovery, agentic commerce, autonomous media, causal measurement, creator commerce, and commerce media lives under `references/2026/`

Those cards are dated evidence, not permanent laws. Re-check platform behavior, availability, eligibility, policy, reporting, pricing, and current product behavior when they are load-bearing

## Deterministic utilities

The repository includes dependency-free Python utilities for calculations and validation, including

- unit economics
- funnel math
- experiment planning
- tactic ranking
- strategy linting
- skill routing
- neural routing
- pack validation
- host package generation
- OpenAI submission bundle generation

Examples

```bash
python scripts/unit_economics.py \
  --revenue-per-order 100 \
  --cogs-per-order 30 \
  --variable-costs-per-order 10 \
  --cac 25 \
  --expected-orders-per-customer 2

python scripts/funnel_math.py visits=1000 leads=100 customers=20
python scripts/experiment_math.py plan --baseline-rate 0.10 --mde 0.02
```

## Security and public distribution

Marketing Council is skills-only for OpenAI distribution. It does not add an MCP server or executable lifecycle hooks merely to increase apparent complexity

Public packaging validation checks for malformed paths, unsafe archive members, transient files, bytecode, secret-shaped files, invalid assets, and other distribution errors

See [`SECURITY.md`](SECURITY.md) for reporting security issues

## Release status language

Keep these states separate

```text
source-valid
package-valid
submission-ready
submitted
approved
published
```

A green repository CI run proves source and package gates. It does not prove that the OpenAI public directory has published the same snapshot

## License

MIT
