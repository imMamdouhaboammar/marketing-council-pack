#!/usr/bin/env python3
"""Build a bounded multi-skill execution DAG without mixing in neural theory routing."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = ROOT / "routing" / "skill-routes.json"
HANDOFFS_PATH = ROOT / "routing" / "skill-handoffs.json"

EXTRA_HINTS = {
    "market-diagnosis": ["diagnose the market", "market structure", "demand problem", "market diagnosis"],
    "customer-research": ["research customers", "customer switching triggers", "buyer interviews", "customer research", "buying language"],
    "competitive-intelligence": ["research competitors", "competitor alternatives", "competitive alternatives", "map competitors", "competitor research"],
    "segmentation-strategy": ["target segments", "choose target segments", "segment the market", "segmentation"],
    "category-strategy": ["category strategy", "category frame", "category maturity"],
    "positioning-strategy": ["position the product", "decide our positioning", "positioning", "competitive frame"],
    "product-marketing": ["product story", "launch message", "product marketing", "product narrative"],
    "offer-strategy": ["offer architecture", "value proposition", "proof architecture", "offer strategy"],
    "pricing-strategy": ["pricing tiers", "set pricing", "pricing architecture", "discount guardrails", "price", "pricing"],
    "go-to-market": ["go-to-market", "go to market", "gtm", "launch sequence", "route to market"],
    "campaign-strategy": ["campaign strategy", "campaign plan", "campaign direction", "campaign job"],
    "media-strategy": ["media strategy", "media plan", "channel roles", "paid distribution", "media"],
    "content-strategy": ["content strategy", "editorial plan", "content plan", "content"],
    "behavioral-marketing": ["behavioral friction", "choice design", "behavioral marketing", "behavior change"],
    "conversion-strategy": ["conversion", "checkout friction", "form abandonment", "cro", "funnel friction"],
    "retention-strategy": ["retention", "churn", "repeat purchase", "reactivation", "lifecycle"],
    "marketing-signal-strategy": ["signal strategy", "crm signals", "offline signals", "value signals"],
    "marketing-measurement": ["measurement architecture", "kpi", "attribution", "measurement"],
    "marketing-experimentation": ["experiment design", "test plan", "a/b test", "ab test", "experimentation"],
    "incrementality-design": ["incrementality", "incremental roas", "geo holdout", "counterfactual", "causal lift"],
    "ai-discovery-strategy": ["ai discovery", "answer surfaces", "ai search", "llm discovery"],
    "conversational-advertising": ["conversational advertising", "conversational ad", "chat ad"],
    "commerce-feed-intelligence": ["product feed", "merchant feed", "feed quality", "feed truth"],
    "agentic-commerce": ["agentic commerce", "shopping agent", "agent-mediated shopping", "agent checkout"],
    "autonomous-media-operations": ["autonomous media", "media automation", "automated bidding authority", "rollback authority"],
    "creator-commerce": ["creator commerce", "creator affiliate", "creator program", "influencer commerce"],
    "commerce-media-strategy": ["commerce media", "retail media", "marketplace media", "closed-loop media"]
}


def _normalise(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip() + " "


def _phrase(text: str, phrase: str) -> bool:
    candidate = _normalise(phrase).strip()
    return bool(candidate) and f" {candidate} " in text


def _load() -> tuple[dict, dict]:
    return (
        json.loads(ROUTES_PATH.read_text(encoding="utf-8")),
        json.loads(HANDOFFS_PATH.read_text(encoding="utf-8")),
    )


def _scores(raw_text: str, routes: dict) -> dict[str, int]:
    text = _normalise(raw_text)
    scores: dict[str, int] = {}
    for route in routes["routes"]:
        slug = route["skill"]
        score = 0
        negatives = route.get("negative_examples", [])
        if any(_phrase(text, item) for item in negatives):
            continue
        phrases = list(route.get("intents", [])) + list(route.get("examples", [])) + EXTRA_HINTS.get(slug, [])
        for item in phrases:
            if _phrase(text, item):
                score += max(2, len(_normalise(item).split()) * 2)
        if score:
            scores[slug] = score
    return scores


def _result(mode: str, primary: str, nodes: list[str], edges: list[list[str]], parallel: list[list[str]], reason: str, confidence: float, fallback: bool) -> dict:
    return {
        "mode": mode,
        "primary_skill": primary,
        "nodes": nodes,
        "edges": edges,
        "parallel_groups": parallel,
        "confidence": round(confidence, 3),
        "reason": reason,
        "fallback": fallback,
    }


def route_dynamic(text: str) -> dict:
    routes, handoffs = _load()
    fallback = routes["fallback_skill"]
    scores = _scores(text, routes)
    ranked = sorted(scores, key=lambda slug: (-scores[slug], slug))
    normalized = _normalise(text)

    if not ranked:
        return _result("council", fallback, [fallback], [], [], "No focused skill has enough explicit evidence to own the request.", 0.3, True)

    strong = [slug for slug in ranked if scores[slug] >= max(4, scores[ranked[0]] * 0.5)]
    has_then = " then " in normalized
    has_parallel = " in parallel " in normalized or " parallel " in normalized
    explicit_sequence = has_then or bool(re.search(r"\bfirst\b.+\bthen\b", normalized))

    if len(strong) == 1 and not explicit_sequence and not has_parallel:
        skill = strong[0]
        return _result("focused", skill, [skill], [], [], "One dominant marketing function has materially stronger request evidence.", min(0.97, 0.72 + scores[skill] / 100), False)

    if not explicit_sequence and not has_parallel:
        return _result("council", fallback, [fallback], [], [], "Several focused skills are plausible but the request does not establish a safe dependency order.", 0.42, True)

    stage = {slug: index for index, slug in enumerate(handoffs["stage_order"])}
    candidates = [slug for slug in ranked if slug in stage]

    # Parallel research is an explicit dependency shape, not an invitation to parallelize everything.
    parallel_groups: list[list[str]] = []
    edges: list[list[str]] = []
    if has_parallel and "positioning-strategy" in candidates:
        upstream = [slug for slug in ("customer-research", "competitive-intelligence") if slug in candidates]
        if len(upstream) == 2:
            nodes = upstream + ["positioning-strategy"]
            parallel_groups = [upstream]
            edges = [[slug, "positioning-strategy"] for slug in upstream]
            return _result("dag", "positioning-strategy", nodes, edges, parallel_groups, "Independent customer and competitor evidence can be collected in parallel before the positioning decision.", 0.88, False)

    ordered = sorted(dict.fromkeys(candidates), key=lambda slug: stage[slug])[: int(handoffs.get("max_nodes", 6))]
    if len(ordered) < 2:
        skill = ordered[0] if ordered else ranked[0]
        return _result("focused", skill, [skill], [], [], "Sequence language was present, but only one focused decision boundary was supported.", 0.69, False)

    # Use explicit stage order only when the request itself asks for a sequence.
    edges = [[ordered[index], ordered[index + 1]] for index in range(len(ordered) - 1)]
    return _result("dag", ordered[-1], ordered, edges, parallel_groups, "The request explicitly asks for dependent marketing decisions, so a bounded execution DAG is justified.", 0.82, False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a bounded Marketing Council skill DAG.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = route_dynamic(args.text)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result)


if __name__ == "__main__":
    main()
