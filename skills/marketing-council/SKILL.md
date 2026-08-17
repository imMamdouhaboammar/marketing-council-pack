---
name: marketing-council
description: Use when a marketing request spans multiple functions, has unclear diagnosis, involves strategic trade-offs, asks for a complete marketing strategy or campaign direction, or needs competing marketing perspectives reconciled into one evidence-backed commercial decision.
license: MIT
compatibility: Host-neutral Agent Skill. Current research, file access, analytics, CRM, ad-platform, browser, or spreadsheet tools are optional and should be used when the host provides them.
metadata:
  version: "1.3.0"
  category: marketing-strategy
---

# Marketing Council

## Core principle

Do not imitate famous marketers. Apply useful decision principles associated with established marketing schools, only when the evidence and market conditions justify them.

A good answer is not the one that sounds most strategic. It is the one that makes the right commercial choice, exposes uncertainty, defines trade-offs, and can be tested.

## Use this skill when

- the user asks for marketing strategy, GTM, launch, campaign, growth, brand, positioning, offer, pricing, media, CRO, or retention work that crosses functions
- the user jumps directly to a tactic before the problem is understood
- different marketing schools could reasonably recommend different actions
- the decision depends on current market, competitor, platform, policy, pricing, or benchmark information
- economics or measurement could invalidate an otherwise attractive idea

For narrow tasks, load the matching focused skill under `../` instead of running the full council.

## Operating sequence

1. **UNDERSTAND**: identify business model, offer, market, objective, time horizon, constraints, available evidence, and requested decision.
2. **DIAGNOSE**: state the commercial or behavioral problem before choosing tactics.
3. **RESEARCH**: when claims may have changed, use current sources or connected data. Never silently treat memory as current evidence.
4. **SIGNAL**: run relevant hooks and convert observations into normalized signals from `../../neural/signals.md`.
5. **ROUTE**: when the task spans multiple plausible schools, use `../../scripts/neural_router.py` with the supported signals and inspect `../../neural/graph.json`.
6. **DISPATCH**: select only the council roles and focused skills that can materially change the decision.
7. **DEBATE**: preserve meaningful disagreements and explicit `counterbalances` connections instead of forcing consensus.
8. **CHALLENGE**: run the marketing skeptic, evidence gate, economics check, and pre-mortem.
9. **DECIDE**: choose one primary strategic direction and explain the deciding factors.
10. **PLAN**: convert the direction into prioritized tactics with owners, thresholds, dependencies, and sequencing where relevant.
11. **EXECUTE**: if the host can act, use only tools the user has authorized and respect confirmation requirements.
12. **MEASURE**: define leading indicators, business outcomes, success thresholds, failure thresholds, and decision dates.
13. **LEARN**: record what changed the decision and what new evidence would reverse it.

## Claim labels

Tag load-bearing statements with one of these statuses when uncertainty matters:

- `FACT`: directly observed or reliably established
- `EVIDENCE`: data or source supporting a claim
- `INFERENCE`: conclusion drawn from evidence
- `ASSUMPTION`: accepted temporarily to proceed
- `HYPOTHESIS`: testable explanation or prediction
- `UNKNOWN`: missing information that materially affects confidence

Never present an assumption as customer insight.

## Council routing

Read the relevant role files in `../../agents/`.

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

Run 2 to 5 roles for most strategic tasks. Use more only when the decision truly spans more functions.

## Execution mode

If the host supports subagents, dispatch selected roles independently from the same evidence brief, then compare their recommendations during debate. Do not let one role's conclusion become another role's premise before independent analysis.

If subagents are unavailable, run the selected role passes serially while keeping each role's diagnosis, assumptions, and recommendation separate until synthesis.

## Principle library

Read only the principle cards relevant to the current decision. The cards are decision aids, not authorities. Always read each card's counterweight before turning a principle into a recommendation.

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

## Neural routing protocol

Use the graph when the diagnosis activates more than one credible school or when the current tactic request may be masking a different constraint.

1. Collect only evidence-supported signals from `../../neural/signals.md`.
2. Run `python ../../scripts/neural_router.py --signals <comma-separated-signals> --json` when scripts are available; otherwise inspect `../../neural/graph.json`.
3. Load the top relevant agent, skill, theory, and principle nodes.
4. Read figure cards under `../../references/figures/` only for source context and boundaries.
5. Preserve active `counterbalances` edges in the debate.
6. Run `../../hooks/theory-fit-gate.md` before making a framework load-bearing.
7. Run `../../hooks/causal-mechanism-check.md` before treating a tactic as likely to cause the business outcome.

The router ranks lenses. It does not decide which lens is true. Evidence and commercial constraints still decide.

## 2026 current-evidence layer

When the decision depends on AI-mediated discovery, agentic commerce, autonomous media, creator commerce, commerce media, or current measurement capabilities, load the matching dated card under `../../references/2026/` before making the platform behavior load-bearing.

- AI search and answer surfaces -> `../../references/2026/ai-mediated-discovery-2026.md`
- agent-mediated shopping and checkout -> `../../references/2026/agentic-commerce-2026.md`
- AI-assisted media execution -> `../../references/2026/autonomous-media-operations-2026.md`
- attribution, incrementality, MMM, and counterfactual design -> `../../references/2026/causal-measurement-2026.md`
- creator discovery, media, and commerce -> `../../references/2026/creator-commerce-2026.md`
- retailer, marketplace, and closed-loop media -> `../../references/2026/commerce-media-2026.md`

Dated evidence is not a timeless marketing law. Re-check availability, eligibility, reporting, policy, and platform behavior before operational recommendations.

## Tool capability contracts

Read `../../tools/capabilities.yml` when binding the skill to host tools. Use host tools by capability, not by hard-coded product name:

- `web.search` or equivalent: current market, competitor, platform, policy, pricing, and benchmark research
- `web.fetch` / browser: source verification and competitor inspection
- `files.search` / `files.read`: briefs, research, prior strategy, CRM exports, reports
- `analytics.query`: behavioral and funnel evidence
- `ads.query`: spend, reach, conversion, audience, creative, placement evidence
- `crm.query`: pipeline, lead quality, sales velocity, loss reasons
- `search-console.query`: search demand and query performance
- `spreadsheet.calculate`: tabular analysis
- deterministic scripts in `../../scripts/`: arithmetic, ranking, linting, validation

If a capability is unavailable, say what evidence is missing and proceed with clearly labeled assumptions only when useful.

## Freshness rule

Treat current market size, competitor behavior, platform features, ad policies, media costs, prices, regulations, availability, trends, benchmarks, and office-holder/company-role facts as potentially stale. Research them before making them load-bearing.

## Conflict resolution

When council roles disagree, write:

- issue
- position A and rationale
- position B and rationale
- deciding factors
- current decision
- confidence from 0 to 1
- evidence that would reverse the decision

Resolve conflicts with evidence, economics, reachability, product truth, customer behavior, constraints, and time horizon. Do not resolve by seniority or name recognition.

## Strategy contract

For a full strategy, produce only sections that add decision value:

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

Every recommended tactic must define:

- objective
- audience
- insight or evidence
- mechanism
- message
- channel
- desired customer action
- expected effect
- cost/effort estimate or unknown
- primary risk
- measurement
- success threshold
- failure threshold
- next action if successful
- next action if unsuccessful

Reject tactics that cannot explain their mechanism or measurement.

## Mandatory challenge gates

Before finalizing a significant strategy, apply:

- `../../hooks/strategy-before-tactics.md`
- `../../hooks/evidence-gate.md`
- `../../hooks/freshness-check.md`
- `../../hooks/commercial-reality-check.md`
- `../../hooks/anti-generic-marketing.md`
- `../../hooks/pre-mortem.md`
- `../../hooks/post-strategy-red-team.md`

Apply these conditionally when their signals are active:

- AI-mediated discovery -> `../../hooks/ai-surface-check.md`
- agentic shopping -> `../../hooks/agentic-commerce-readiness.md` and `../../hooks/commerce-feed-readiness.md`
- autonomous execution -> `../../hooks/automation-authority-check.md` and `../../hooks/automation-black-box-check.md`
- weak optimization signals -> `../../hooks/marketing-signal-quality.md`
- causal spend decisions -> `../../hooks/incrementality-required.md`
- synthetic or creator-derived assets -> `../../hooks/creative-provenance-check.md`
- creator programs -> `../../hooks/creator-measurement-check.md`
- closed-loop commerce media -> `../../hooks/closed-loop-bias-check.md`

## Quality failures

Stop and revise if the answer:

- could be sent unchanged to five unrelated businesses
- recommends a channel because it is popular rather than suitable
- uses demographics as a substitute for buying behavior
- treats reach, engagement, or traffic as business outcomes without a causal link
- invents customer psychology or market facts
- ignores margin, capacity, retention, or payback when they matter
- produces a long tactic list without a primary strategic choice
- hides uncertainty
- fabricates proof, urgency, scarcity, testimonials, benchmarks, or research

## Focused skills

Load a focused sibling skill when the task centers on one function:

`market-diagnosis`, `customer-research`, `segmentation-strategy`, `positioning-strategy`, `category-strategy`, `brand-strategy`, `product-marketing`, `offer-strategy`, `pricing-strategy`, `go-to-market`, `campaign-strategy`, `media-strategy`, `content-strategy`, `behavioral-marketing`, `conversion-strategy`, `retention-strategy`, `competitive-intelligence`, `marketing-measurement`, `marketing-experimentation`, `ai-discovery-strategy`, `conversational-advertising`, `agentic-commerce`, `commerce-feed-intelligence`, `autonomous-media-operations`, `marketing-signal-strategy`, `incrementality-design`, `creator-commerce`, and `commerce-media-strategy`.

Use `../../workflows/full-strategy.md` for an end-to-end engagement and `../../workflows/council-debate.md` when conflicting recommendations are central.

## Neural connections

- Principles: `counterweight-required`, `evidence-status`, `commercial-reality`
- Applied theories: `marketing-management`, `marketing-effectiveness`, `behavioral-science`
- Router: `../../neural/graph.json` and `../../scripts/neural_router.py`
- Use `../../hooks/theory-fit-gate.md` when more than one theory could plausibly explain the problem.
