<div align="center">

<img src="assets/logo.svg" alt="Marketing Council" width="108" height="108" />

# Marketing Council

### Stop asking AI for marketing ideas. Make it defend a marketing decision.

**29 Agent Skills. 24 specialist agents. 25 marketing figures. 46 applied theories. One connected decision process.**

Marketing Council makes ChatGPT, Codex, Claude Code, and compatible AI agents diagnose the business problem, compare competing strategic views, check evidence and economics, challenge weak assumptions, and only then recommend tactics.

[![Version](https://img.shields.io/badge/version-1.3.0-173F35)](CHANGELOG.md)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-20-173F35)](skills/)
[![Specialist Agents](https://img.shields.io/badge/Specialist%20Agents-18-173F35)](agents/)
[![License](https://img.shields.io/badge/license-MIT-173F35)](LICENSE)

</div>

## The Neural Marketing Graph

Marketing Council v1.2 adds an explicit connection graph instead of leaving theory selection hidden inside prompts.

```text
HOOKS -> SIGNALS -> SCHOOLS / THEORIES -> AGENTS -> SKILLS -> CHALLENGE -> DECISION
```

The graph currently connects:

- **25 marketing figures and practitioners** as source-linked decision cards
- **19 schools of thought**
- **44 principles**
- **46 applied theories**
- **23 diagnostic signals**
- **24 specialist agents**
- **29 focused skills**
- **14 challenge hooks**
- **682 explicit connections**

This means a mature category with weak differentiation can activate positioning and competitive-strategy specialists, while a conversion problem caused by friction can route toward behavioral diagnosis instead of automatically asking for stronger copy.

Try the deterministic router:

```bash
python scripts/neural_router.py \
  --signals category-mature,differentiation-weak,competitor-pressure-high \
  --json
```

The graph also stores explicit counterweights. A narrow-entry-audience principle can be challenged by penetration-growth logic; short-response accountability can be challenged by longer-horizon effectiveness; positioning focus can be challenged by broad mental-availability requirements.

## Marketing schools in the graph

The figure cards are not personas. They are source pointers into different ways of making marketing decisions.

| School | Figures represented | What it changes |
|---|---|---|
| Marketing management | Philip Kotler, Kevin Lane Keller | Market definition, STP, value and mix decisions |
| Customer-centered market definition | Theodore Levitt, Peter Drucker | What business and customer problem are actually being served |
| Positioning and category strategy | Al Ries, Jack Trout, April Dunford | Competitive alternatives, category frame, reason to prefer |
| Direct response and scientific advertising | Claude Hopkins, David Ogilvy, Rosser Reeves | Offer, proof, proposition, testing, response |
| Awareness and sophistication | Eugene Schwartz | Message depth, mechanism, proof burden, directness |
| Marketing science and brand growth | Andrew Ehrenberg, Byron Sharp | Penetration, mental availability, physical availability, buying patterns |
| Brand equity | David Aaker, Kevin Lane Keller | Associations, salience, perceived quality, brand architecture |
| Behavioral science and choice design | Robert Cialdini, BJ Fogg, Richard Thaler, Rory Sutherland | Friction, prompts, defaults, framing, uncertainty |
| Creative advertising | Bill Bernbach, David Ogilvy, Rory Sutherland | Translation from strategy into attention and memorable communication |
| Product narrative and demonstration | Steve Jobs | Focus, demonstration, product truth, launch story |
| Permission and remarkability | Seth Godin | Entry audience, relevance, voluntary attention |
| Competitive strategy | Michael Porter | Substitutes, rivalry, bargaining power, defensibility |
| Marketing effectiveness | Les Binet, Peter Field | Short and longer horizons, business effects, objective balance |
| Jobs to Be Done | Clayton Christensen | Buying circumstances, progress, switching triggers, alternatives |

A named figure can never settle a debate. The graph carries the principle into the decision, then applies a counterweight when another school has a credible competing explanation.

## 2026 AI-mediated marketing layer

Version 1.3 adds a dated evidence layer for market changes that should not be confused with timeless marketing theory. The neural router can now activate dedicated paths for:

- AI-mediated search, answer surfaces, and conversational advertising
- Agentic commerce, machine-readable product truth, and commerce-feed readiness
- Autonomous media decision rights, signal quality, and rollback governance
- Incrementality, MMM, counterfactual design, and closed-loop bias
- Creator commerce and creator-role-specific measurement
- Commerce media across retailers, marketplaces, social commerce, and purchase-data environments
- Synthetic creative hypothesis families and provenance checks

Current platform claims live under `references/2026/` with dated source IDs. The Council must re-check those facts when they are load-bearing.


## The problem

Most AI marketing sessions collapse into the same pattern:

> "Try short-form video. Build awareness. Create valuable content. Test different creatives. Track KPIs."

That is not strategy. It is a list of familiar activities.

Marketing Council changes the sequence.

```text
UNDERSTAND
  -> DIAGNOSE
  -> RESEARCH
  -> DISPATCH
  -> DEBATE
  -> CHALLENGE
  -> DECIDE
  -> PLAN
  -> EXECUTE
  -> MEASURE
  -> LEARN
```

If the evidence says the requested tactic is wrong, the Council should reject it. If the economics do not support the campaign, it should say so. If two marketing schools point in different directions, it should preserve the disagreement until the deciding factors are clear.

## Install in 30 seconds

### Any agent supported by Skills CLI

Install every Marketing Council skill to every supported agent:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --all -y
```

See what the repository contains before installing:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --list
```

Install all skills globally for Codex only:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a codex -y
```

Install all skills globally for Claude Code only:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill '*' -g -a claude-code -y
```

Install only the main Council skill:

```bash
npx skills add imMamdouhaboammar/marketing-council-pack --skill marketing-council -g -y
```

Run the main skill without installing it:

```bash
npx skills use imMamdouhaboammar/marketing-council-pack --skill marketing-council --agent codex
```

Update installed global skills:

```bash
npx skills update -g -y
```

> `npx skills` installs Agent Skills. For Claude's 18 native specialist subagents, use the Claude marketplace installation below.

## ChatGPT + Codex plugin

Marketing Council includes a native `.codex-plugin/plugin.json`, OpenAI metadata for all 29 skills, repository marketplace metadata, brand assets, and the 24 specialist role files used by the Council.

Add the repository marketplace:

```bash
codex plugin marketplace add imMamdouhaboammar/marketing-council-pack
```

Inspect or refresh it:

```bash
codex plugin marketplace list
codex plugin marketplace upgrade marketing-council
```

In the ChatGPT desktop app, open the Plugins Directory, select the **Marketing Council** marketplace, and install the plugin.

Build a standalone OpenAI plugin ZIP:

```bash
python scripts/build_host_packages.py
```

Output:

```text
dist/release/marketing-council-openai-plugin-v1.3.0.zip
```

The OpenAI package is skills-only. It does not invent an MCP server or executable lifecycle hook just to make the manifest look more complex.

## Claude Code marketplace

The Claude plugin exposes both sides of Marketing Council:

- all 29 skills under `skills/`
- all 18 role definitions as native Claude subagents under `agents/`

Inside Claude Code:

```text
/plugin marketplace add imMamdouhaboammar/marketing-council-pack
/plugin install marketing-council@marketing-council
```

Validate a local checkout:

```bash
claude plugin validate . --strict
```

Build a standalone local marketplace ZIP:

```bash
python scripts/build_host_packages.py
```

Output:

```text
dist/release/marketing-council-claude-marketplace-v1.3.0.zip
```

That archive is self-contained. Its marketplace points to a local `./plugins/marketing-council` copy, so the plugin, skills, agents, references, and scripts travel together.

## What happens when you ask a marketing question

Say you ask:

> "Conversion is weak. I want to cut price by 20% and go hard on TikTok. Build the plan."

A generic assistant can start writing TikTok ideas immediately.

Marketing Council should first work out whether the real problem is demand, traffic quality, offer clarity, pricing, checkout friction, product fit, or retention. It can then route the same evidence brief to the relevant roles, for example:

```text
market-architect
commercial-strategist
channel-strategist
response-strategist
marketing-skeptic
```

The Council then has to answer questions such as:

- Is price actually suppressing conversion?
- What happens to contribution margin and CAC payback after the cut?
- Is TikTok where this buying situation happens, or merely the requested channel?
- What evidence supports the audience claim?
- What would make us abandon the recommendation?
- What are we explicitly choosing not to do?

The result is a decision with assumptions, risks, thresholds, and next actions, not a longer brainstorm.

## Built from marketing schools, not celebrity role-play

Marketing Council does not assign celebrity identities to the AI model. Philip Kotler, Seth Godin, David Ogilvy, Claude Hopkins, Eugene Schwartz, Al Ries, Jack Trout, Robert Cialdini, Byron Sharp, Les Binet, Peter Field, Steve Jobs, and other named thinkers appear only as sources or reference points for decision principles.

Instead, the repository turns useful ideas associated with established marketing schools into decision cards with four practical fields:

```text
Principle
When it applies
When it should not be over-applied
What evidence or competing principle should challenge it
```

Examples live in [`references/canon/`](references/canon/).

The point is not asking for a famous marketer's imagined response. The useful question is:

> Which principle fits this evidence, under these market conditions and commercial constraints, and what would falsify the recommendation?

This is an independent project and is not affiliated with or endorsed by the authors, estates, publishers, or companies referenced in the principle library.

## The Council

### Market and customer

| Agent | Job |
|---|---|
| `market-architect` | Market definition, segmentation, category structure, demand, route to market |
| `audience-strategist` | Buying situations, jobs, triggers, anxieties, alternatives, customer language |
| `positioning-strategist` | Category frame, alternatives, differentiation, memory |
| `product-marketing-director` | Product truth, focus, demonstration, launch narrative |

### Persuasion and behavior

| Agent | Job |
|---|---|
| `response-strategist` | Offer, proof, objections, CTA, measurable response |
| `awareness-strategist` | Awareness, sophistication, message depth, proof requirements |
| `behavior-strategist` | Friction, choice architecture, risk, social proof, decision cues |

### Growth and commercial reality

| Agent | Job |
|---|---|
| `brand-growth-strategist` | Reach, penetration, availability, distinctive assets, time horizon |
| `commercial-strategist` | Price, margin, CAC, LTV, payback, retention, sales capacity |
| `channel-strategist` | Media, search, creators, partnerships, distribution and channel fit |

### Governance

| Agent | Job |
|---|---|
| `marketing-skeptic` | Finds weak evidence, hidden assumptions, channel bias, fake certainty |
| `council-director` | Selects roles, preserves disagreements, resolves the final decision |

## 14 installable skills

The repository is deliberately modular. A narrow task should not load an entire strategy engagement.

```text
marketing-council
market-diagnosis
customer-research
positioning-strategy
offer-strategy
pricing-strategy
go-to-market
campaign-strategy
media-strategy
content-strategy
conversion-strategy
retention-strategy
marketing-experimentation
competitive-intelligence
```

The main `marketing-council` skill routes broad or conflicted work. The other 13 skills handle focused jobs with less context.

## Eight challenge gates

Before a significant recommendation is accepted, the pack can apply:

1. `strategy-before-tactics`
2. `evidence-gate`
3. `freshness-check`
4. `commercial-reality-check`
5. `customer-language-check`
6. `anti-generic-marketing`
7. `pre-mortem`
8. `post-strategy-red-team`

These are reasoning gates stored as marketing guidance. They are not hidden shell commands or auto-running lifecycle hooks.

## Evidence has a status

Load-bearing statements can be labeled as:

```text
FACT
EVIDENCE
INFERENCE
ASSUMPTION
HYPOTHESIS
UNKNOWN
```

That small constraint matters. "Customers value authenticity" cannot quietly become customer research when nobody actually observed it.

## Strategy means choosing

A full Council output can cover:

1. Situation
2. Decision to make
3. Evidence map
4. Diagnosis
5. Audience and buying situation
6. Positioning and category frame
7. Value proposition and offer
8. Primary strategic choice
9. What we will not do
10. Channel and distribution strategy
11. Message architecture
12. Prioritized tactics
13. Experiments
14. Measurement and thresholds
15. Risks and assumptions
16. Next decisions

The ninth item is intentional. A strategy that refuses to exclude anything is usually a backlog.

## Tactics need a mechanism

Every recommended tactic is expected to define:

```text
objective
customer / audience
evidence or insight
mechanism
message
channel
desired action
expected effect
cost or effort
primary risk
measurement
success threshold
failure threshold
next action if it works
next action if it does not
```

If a tactic cannot explain why it should work or how failure will be detected, it is not ready.

## Deterministic marketing utilities

Some decisions should use arithmetic instead of prose. The pack includes dependency-free Python utilities for:

- unit economics
- funnel rates
- experiment sample-size planning
- tactic ranking
- strategy linting
- pack and distribution validation

Examples:

```bash
python scripts/unit_economics.py \
  --revenue-per-order 100 \
  --cogs-per-order 30 \
  --variable-costs-per-order 10 \
  --cac 25 \
  --expected-orders-per-customer 2

python scripts/funnel_math.py visits=1000 leads=100 customers=20
python scripts/experiment_math.py plan --baseline-rate 0.10 --mde 0.02
python scripts/strategy_linter.py path/to/strategy.md
```

## Tool contracts, not hard-coded vendors

Marketing Council describes capabilities such as:

```text
web.search
web.fetch
files.search
files.read
analytics.query
ads.query
crm.query
search-console.query
spreadsheet.calculate
```

A host can bind those capabilities to whatever tools it actually has. If a capability is missing, the skill should expose the evidence gap rather than pretend the data was checked.

See [`tools/capabilities.yml`](tools/capabilities.yml).

## Evals are part of the product

The repository includes 8 business cases and 6 adversarial cases.

They test whether the agent:

- diagnoses before prescribing
- changes its recommendation when the business conditions change
- separates evidence from assumptions
- lets economics affect the decision
- distinguishes strategy from tactics
- rejects requested-channel bias
- refuses invented customer insight and fake scarcity
- does not treat attribution as causation
- exposes uncertainty

See [`evals/`](evals/).

## Build releases

Build every host package plus the source archive:

```bash
python scripts/build_host_packages.py
```

Generated files:

```text
marketing-council-openai-plugin-v1.3.0.zip
marketing-council-claude-marketplace-v1.3.0.zip
marketing-council-skill-v1.3.0.zip
marketing-council-pack-v1.3.0.zip
marketing-council-v1.3.0-SHA256SUMS.txt
```

Build only the single self-contained Agent Skill directory:

```bash
python scripts/build_dist.py
```

## Validate

```bash
python -m unittest discover -s tests -v
python scripts/validate_pack.py
python scripts/validate_distribution.py --json
```

For an extracted OpenAI plugin package:

```bash
python scripts/validate_openai_plugin.py path/to/extracted/plugin --json
```

When Claude Code is installed locally:

```bash
claude plugin validate . --strict
```

## Repository map

```text
marketing-council-pack/
├── .agents/plugins/          # ChatGPT/Codex repo marketplace
├── .codex-plugin/            # ChatGPT/Codex plugin manifest
├── .claude-plugin/           # Claude plugin + marketplace manifests
├── assets/                   # Plugin identity
├── skills/                   # 29 Agent Skills
├── agents/                   # 24 specialist role definitions
├── hooks/                    # Marketing challenge gates, not lifecycle hooks
├── workflows/                # Full strategy, launch, campaign, audit, debate
├── references/               # Figures, schools, principles, theories, canon, frameworks
├── neural/                   # Knowledge graph, signals, routing guide
├── tools/                    # Host-neutral tool capability contracts
├── scripts/                  # Math, linting, builders, validators
├── evals/                    # Core and adversarial scenarios
├── examples/                 # Example strategy and council debate
├── adapters/                 # Host-specific usage notes
└── tests/                    # Structural and behavioral checks
```

## Good prompts to start with

```text
Diagnose this marketing problem before recommending tactics: [context]
```

```text
Run a council debate on this strategy. Show where the specialists disagree, what decides the disagreement, and what evidence would reverse the final recommendation: [strategy]
```

```text
Red-team this marketing plan. Find unsupported assumptions, commercial risks, channel bias, and weak measurement. Then rebuild only the parts that fail: [plan]
```

```text
Build a go-to-market strategy for [product] in [market]. Separate facts, evidence, assumptions, hypotheses, and unknowns. Research current facts before making them load-bearing.
```

## Security and privacy

Marketing Council ships without credentials, tracking code, an MCP server, or executable lifecycle hooks. Host tools and connected data remain subject to the host's own permissions and user authorization.

See [`SECURITY.md`](SECURITY.md).

## License

MIT. See [`LICENSE`](LICENSE).
