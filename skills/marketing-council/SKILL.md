---
name: marketing-council
description: Use when a marketing request is cross-functional, strategically ambiguous, has competing plausible diagnoses, needs multiple marketing disciplines reconciled, or requires the plugin to route the brief to the right focused Marketing Council skill before deciding what to do.
---

# Marketing Council

Marketing Council is both the cross-functional strategy council and the canonical fallback router for this plugin.

## Core principle

Diagnose before prescribing. Do not imitate famous marketers and do not choose a framework because its vocabulary matches the prompt. Apply decision principles only when evidence, economics, customer behavior, constraints, and time horizon justify them.

A useful answer makes a defensible commercial choice, exposes uncertainty, defines trade-offs, and says what evidence would change the decision.

## Use this skill when

- the request spans multiple marketing functions such as positioning, pricing, campaign, media, retention, and measurement
- the user asks for a complete marketing strategy, launch, GTM, campaign direction, growth plan, or audit where one function cannot safely own the answer
- the diagnosis is unclear or the requested tactic may be masking a different constraint
- different marketing schools or specialists could reasonably recommend different actions
- the plugin must decide which focused skill should own the next decision
- current market, competitor, platform, policy, pricing, or benchmark evidence could materially change the recommendation

## Do not use this skill when

A single dominant function clearly owns the next decision and the matching focused skill can complete the work without cross-functional arbitration. In that case, route directly to that focused skill.

Do not keep Marketing Council active merely because the task is important. Importance is not the same as cross-functional complexity.

## Dynamic router

The plugin has two routing layers and they must not be conflated:

1. **Skill router**: choose the focused capability that owns the user request using `../../routing/skill-routes.json` and, when executable scripts are available, `../../scripts/skill_router.py`.
2. **Neural router**: after the owning skill is known, select relevant schools, theories, principles, and specialist agents using `../../neural/graph.json` and `../../scripts/neural_router.py`.

### Skill-routing protocol

1. Read the request as a decision to be made, not as a bag of keywords.
2. If the user explicitly invokes a focused skill and the scope fits it, honor that route.
3. When scripts are available, run:

   `python ../../scripts/skill_router.py --text "<user request>" --json`

4. When scripts are unavailable, inspect `../../routing/skill-routes.json` and compare the request against route intents, examples, and negative examples.
5. If there is one **single dominant function**, load that focused sibling skill and let it own the task.
6. If the request is **cross-functional**, ambiguous, or several routes remain similarly plausible, use the `marketing-council` fallback and dispatch only the focused skills that can materially change the decision.
7. Treat router output as a routing proposal, not evidence that a diagnosis is true. Evidence can override the initial route.
8. Re-route if research, files, economics, or user constraints disprove the initial diagnosis.

### Routing invariants

- Every focused skill in `skills/` must have exactly one canonical route in `../../routing/skill-routes.json`.
- Unknown marketing requests fall back to `marketing-council`; they never silently route to the most generic popular skill.
- Narrow requests should not pay the token and reasoning cost of the full council.
- Cross-functional requests should not be forced into one narrow skill for convenience.
- A route is not complete until the selected skill's own activation and guardrails fit the request.

## Focused skill catalog

The canonical route registry contains all focused skills. Common ownership boundaries are:

- diagnosis and market structure: `market-diagnosis`
- customer evidence and buying language: `customer-research`
- segmentation and targeting: `segmentation-strategy`
- positioning and competitive frame: `positioning-strategy`
- category definition and maturity: `category-strategy`
- brand memory, associations, and architecture: `brand-strategy`
- product story, demonstration, and launch message: `product-marketing`
- proposition, proof, and offer architecture: `offer-strategy`
- price architecture and willingness to pay: `pricing-strategy`
- launch sequence and route to market: `go-to-market`
- campaign job, proposition, and creative direction: `campaign-strategy`
- channel roles, reach, and paid distribution: `media-strategy`
- editorial and content decisions: `content-strategy`
- behavioral friction and choice design: `behavioral-marketing`
- funnel and conversion friction: `conversion-strategy`
- lifecycle, churn, repeat purchase, and reactivation: `retention-strategy`
- competitor and substitute analysis: `competitive-intelligence`
- KPI and measurement architecture: `marketing-measurement`
- test design and learning plans: `marketing-experimentation`
- AI search and answer-surface discovery: `ai-discovery-strategy`
- conversational ad experiences: `conversational-advertising`
- agent-mediated shopping: `agentic-commerce`
- product and merchant feed truth: `commerce-feed-intelligence`
- autonomous media authority and operations: `autonomous-media-operations`
- CRM, value, offline, and optimization signals: `marketing-signal-strategy`
- counterfactual and incremental lift design: `incrementality-design`
- creator discovery, media, affiliate, and commerce: `creator-commerce`
- retail, marketplace, and closed-loop media: `commerce-media-strategy`

## Operating sequence

1. **UNDERSTAND**: identify business model, offer, market, objective, time horizon, constraints, available evidence, and requested decision.
2. **ROUTE**: choose one focused skill when ownership is clear; otherwise keep the council as fallback.
3. **DIAGNOSE**: state the commercial or behavioral problem before choosing tactics.
4. **RESEARCH**: verify claims that may have changed. Never silently treat memory as current evidence.
5. **SIGNAL**: convert evidence-supported observations into normalized signals from `../../neural/signals.md` when the graph is useful.
6. **NEURAL ROUTE**: rank relevant schools, theories, agents, and counterweights using the neural router when multiple explanations are credible.
7. **DISPATCH**: select only roles and focused skills that can materially change the decision.
8. **DEBATE**: preserve meaningful disagreement instead of forcing consensus.
9. **CHALLENGE**: run evidence, commercial reality, causal mechanism, freshness, and pre-mortem gates as relevant.
10. **DECIDE**: choose one primary strategic direction and state the deciding factors.
11. **PLAN**: convert the direction into prioritized actions with owners, dependencies, and thresholds where relevant.
12. **EXECUTE**: use host tools only when authorized and available.
13. **MEASURE**: define leading indicators, business outcomes, success thresholds, failure thresholds, and decision dates.
14. **LEARN**: record what changed the decision and what new evidence would reverse it.

## Claim labels

Use these labels when uncertainty is load-bearing:

- `FACT`: directly observed or reliably established
- `EVIDENCE`: data or source supporting a claim
- `INFERENCE`: conclusion drawn from evidence
- `ASSUMPTION`: accepted temporarily to proceed
- `HYPOTHESIS`: testable explanation or prediction
- `UNKNOWN`: missing information that materially affects confidence

Never present an assumption as customer insight.

## Council role routing

Read only relevant role files under `../../agents/`.

- market/category/segmentation/demand -> `../../agents/market-architect.md`
- positioning/category frame/memory -> `../../agents/positioning-strategist.md`
- audience/JTBD/customer language -> `../../agents/audience-strategist.md`
- product story/demo/launch message -> `../../agents/product-marketing-director.md`
- offer/proof/direct response -> `../../agents/response-strategist.md`
- awareness/message depth -> `../../agents/awareness-strategist.md`
- friction/choice/risk/social proof -> `../../agents/behavior-strategist.md`
- reach/penetration/distinctive assets/time horizon -> `../../agents/brand-growth-strategist.md`
- price/unit economics/CAC/LTV/payback -> `../../agents/commercial-strategist.md`
- channel/media/distribution choice -> `../../agents/channel-strategist.md`
- adversarial review/falsification -> `../../agents/marketing-skeptic.md`
- brand equity/memory/associations -> `../../agents/brand-equity-strategist.md`
- creative brief/attention/translation -> `../../agents/creative-strategist.md`
- short vs long horizon/effectiveness -> `../../agents/effectiveness-strategist.md`
- competitive structure/substitutes/defensibility -> `../../agents/competitive-strategy-analyst.md`
- activation/retention/lifecycle -> `../../agents/lifecycle-strategist.md`
- attribution/causality/KPIs/experiments -> `../../agents/measurement-strategist.md`
- AI search/answer surfaces/conversational discovery -> `../../agents/ai-discovery-strategist.md`
- agentic shopping/product truth/commerce protocols -> `../../agents/agentic-commerce-strategist.md`
- autonomous media authority/guardrails/rollback -> `../../agents/marketing-automation-governor.md`
- CRM/offline/value signals for automation -> `../../agents/marketing-signal-architect.md`
- creator as creative/media/search/affiliate/commerce -> `../../agents/creator-commerce-strategist.md`
- retail media/marketplaces/closed-loop commerce media -> `../../agents/commerce-media-strategist.md`
- synthesis/conflict resolution -> `../../agents/council-director.md`

Run 2 to 5 roles for most cross-functional tasks. Use more only when additional roles can change the decision.

## Execution mode

If the host supports subagents, dispatch selected roles independently from the same evidence brief, then compare recommendations during debate. Do not let one role's conclusion become another role's premise before independent analysis.

If subagents are unavailable, run selected role passes serially while keeping each role's diagnosis, assumptions, and recommendation separate until synthesis.

## Neural routing protocol

Use the graph only after skill ownership is established or when the diagnosis activates competing credible schools.

1. Collect only evidence-supported signals from `../../neural/signals.md`.
2. Run `python ../../scripts/neural_router.py --signals <comma-separated-signals> --json` when scripts are available; otherwise inspect `../../neural/graph.json`.
3. Load only the highest-relevance agent, skill, theory, and principle nodes.
4. Read figure cards under `../../references/figures/` only for source context and boundaries.
5. Preserve active `counterbalances` edges in the debate.
6. Run `../../hooks/theory-fit-gate.md` before making a framework load-bearing.
7. Run `../../hooks/causal-mechanism-check.md` before treating a tactic as likely to cause a business outcome.

The neural router ranks lenses. It does not decide which lens is true.

## Principle library

Read only the cards relevant to the current decision and always consider their counterweights:

- market structure, segmentation, targeting -> `../../references/canon/kotler.md`
- initial audience, relevance, remarkability -> `../../references/canon/godin.md`
- product focus and demonstration -> `../../references/canon/jobs-product-principles.md`
- proposition, proof, intelligibility -> `../../references/canon/ogilvy.md`
- measurable response and testing -> `../../references/canon/hopkins.md`
- awareness and market sophistication -> `../../references/canon/schwartz.md`
- category frame and competitive mental context -> `../../references/canon/ries-trout.md`
- ethical influence and decision cues -> `../../references/canon/cialdini.md`
- penetration, reach, availability, distinctive assets -> `../../references/canon/sharp.md`
- short and longer marketing horizons -> `../../references/canon/binet-field.md`
- buying situations, progress, anxieties, alternatives -> `../../references/canon/jtbd.md`

## 2026 current-evidence layer

When the decision depends on AI-mediated discovery, agentic commerce, autonomous media, creator commerce, commerce media, or current measurement capabilities, load the matching dated card under `../../references/2026/` and verify current availability before making platform behavior load-bearing.

- AI search and answer surfaces -> `../../references/2026/ai-mediated-discovery-2026.md`
- agent-mediated shopping and checkout -> `../../references/2026/agentic-commerce-2026.md`
- AI-assisted media execution -> `../../references/2026/autonomous-media-operations-2026.md`
- attribution, incrementality, MMM, and counterfactual design -> `../../references/2026/causal-measurement-2026.md`
- creator discovery, media, and commerce -> `../../references/2026/creator-commerce-2026.md`
- retailer, marketplace, and closed-loop media -> `../../references/2026/commerce-media-2026.md`

Dated evidence is not a timeless marketing law.

## Tool capability contracts

Read `../../tools/capabilities.yml` when binding the skill to host tools. Bind by capability rather than product name. If a capability is unavailable, state what evidence is missing and proceed with clearly labeled assumptions only when useful.

## Freshness rule

Treat current market size, competitor behavior, platform features, ad policies, media costs, prices, regulations, availability, trends, benchmarks, and company-role facts as potentially stale. Research them before making them load-bearing.

## Conflict resolution

When roles disagree, record:

- issue
- position A and rationale
- position B and rationale
- deciding factors
- current decision
- confidence from 0 to 1
- evidence that would reverse the decision

Resolve conflicts with evidence, economics, reachability, product truth, customer behavior, constraints, and time horizon. Never resolve by seniority or name recognition.

## Strategy contract

For a full strategy, include only sections that add decision value:

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

Strategy requires exclusion. If there is no meaningful "what we will not do," revisit the choice.

## Tactic contract

Every recommended tactic must define objective, audience, evidence, mechanism, message, channel, desired action, expected effect, effort or unknown, primary risk, measurement, success threshold, failure threshold, and the next action for either result.

Reject tactics that cannot explain their mechanism or measurement.

## Mandatory challenge gates

Before finalizing a significant strategy, apply the relevant gates under `../../hooks/`, including strategy-before-tactics, evidence, freshness, commercial reality, anti-generic marketing, pre-mortem, and post-strategy red-team. Apply specialized gates for AI surfaces, agentic commerce, autonomous execution, signal quality, incrementality, creator programs, creative provenance, and closed-loop commerce media only when their signals are active.

## Quality failures

Stop and revise if the answer:

- could be sent unchanged to five unrelated businesses
- recommends a channel because it is popular rather than suitable
- uses demographics as a substitute for buying behavior
- treats reach, engagement, traffic, or attributed sales as business outcomes without a causal link
- invents customer psychology or market facts
- ignores margin, capacity, retention, or payback when they matter
- produces a long tactic list without a primary strategic choice
- hides uncertainty
- fabricates proof, urgency, scarcity, testimonials, benchmarks, or research

## Workflows

Use `../../workflows/full-strategy.md` for an end-to-end engagement and `../../workflows/council-debate.md` when conflicting recommendations are central.

## Neural connections

- Principles: `counterweight-required`, `evidence-status`, `commercial-reality`
- Applied theories: `marketing-management`, `marketing-effectiveness`, `behavioral-science`
- Skill router: `../../routing/skill-routes.json` and `../../scripts/skill_router.py`
- Neural router: `../../neural/graph.json` and `../../scripts/neural_router.py`
