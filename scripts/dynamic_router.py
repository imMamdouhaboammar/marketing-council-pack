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

AMBIGUITY_MARKERS = (
    "cannot tell",
    "can't tell",
    "do not know whether",
    "don't know whether",
    "not sure whether",
    "unclear whether",
    "which problem is primary",
    "which issue is primary",
)


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


def _route_matches(raw_text: str, routes: dict) -> tuple[dict[str, int], dict[str, int]]:
    text = _normalise(raw_text)
    scores: dict[str, int] = {}
    positions: dict[str, int] = {}
    for route in routes["routes"]:
        slug = route["skill"]
        score = 0
        first_position: int | None = None
        negatives = route.get("negative_examples", [])
        if any(_phrase(text, item) for item in negatives):
            continue
        phrases = list(route.get("intents", [])) + list(route.get("examples", [])) + EXTRA_HINTS.get(slug, [])
        for item in phrases:
            candidate = _normalise(item).strip()
            if not candidate:
                continue
            position = text.find(f" {candidate} ")
            if position < 0:
                continue
            score += max(2, len(candidate.split()) * 2)
            first_position = position if first_position is None else min(first_position, position)
        if score:
            scores[slug] = score
            positions[slug] = first_position if first_position is not None else len(text)
    return scores, positions


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
    scores, positions = _route_matches(text, routes)
    ranked = sorted(scores, key=lambda slug: (-scores[slug], slug))
    normalized = _normalise(text)

    if not ranked:
        return _result("council", fallback, [fallback], [], [], "No focused skill has enough explicit evidence to own the request.", 0.3, True)

    strong = [slug for slug in ranked if scores[slug] >= max(4, scores[ranked[0]] * 0.5)]
    has_then = " then " in normalized
    has_parallel = " in parallel " in normalized or " parallel " in normalized
    explicit_sequence = has_then or bool(re.search(r"\bfirst\b.+\bthen\b", normalized))
    explicit_uncertainty = any(marker in normalized for marker in AMBIGUITY_MARKERS)

    if explicit_uncertainty and len(ranked) >= 2 and not explicit_sequence and not has_parallel:
        return _result("council", fallback, [fallback], [], [], "The request explicitly states that ownership is uncertain across multiple plausible problems.", 0.4, True)

    if len(strong) == 1 and not explicit_sequence and not has_parallel:
        skill = strong[0]
        return _result("focused", skill, [skill], [], [], "One dominant marketing function has materially stronger request evidence.", min(0.97, 0.72 + scores[skill] / 100), False)

    if not explicit_sequence and not has_parallel:
        return _result("council", fallback, [fallback], [], [], "Several focused skills are plausible but the request does not establish a safe dependency order.", 0.42, True)

    max_nodes = int(handoffs.get("max_nodes", 6))
    requested = sorted(
        dict.fromkeys(ranked),
        key=lambda slug: (positions.get(slug, 10**9), -scores[slug], slug),
    )
    declared_handoffs = {
        (item["from"], item["to"])
        for item in handoffs.get("handoffs", [])
    }
    parallel_safe = [
        tuple(group)
        for group in handoffs.get("parallel_safe", [])
        if len(group) == 2
    ]

    # Parallel execution is allowed only when the declared configuration marks
    # the pair safe and both branches converge through declared handoffs. Any
    # sequential tail after the fan-in must also consume every explicitly
    # requested Skill through declared handoffs; nothing may be dropped.
    if has_parallel:
        for pair in parallel_safe:
            if not all(slug in requested for slug in pair):
                continue

            pair_start = min(positions.get(slug, -1) for slug in pair)
            cutoff = max(positions.get(slug, -1) for slug in pair)
            common_targets = [
                slug
                for slug in requested
                if slug not in pair
                and positions.get(slug, -1) > cutoff
                and all((upstream, slug) in declared_handoffs for upstream in pair)
            ]
            if not common_targets:
                continue

            target = common_targets[0]
            target_position = positions.get(target, 10**9)
            tail = [
                slug
                for slug in requested
                if slug not in pair
                and slug != target
                and positions.get(slug, -1) > target_position
            ]
            consumed = set(pair) | {target} | set(tail)
            unconsumed = [slug for slug in requested if slug not in consumed]
            if unconsumed or any(
                slug not in pair and positions.get(slug, 10**9) < pair_start
                for slug in requested
            ):
                return _result(
                    "council",
                    fallback,
                    [fallback],
                    [],
                    [],
                    "The parallel request contains additional Skills that cannot be placed without reordering or dropping an explicit dependency.",
                    0.4,
                    True,
                )

            nodes = list(pair) + [target] + tail
            if len(nodes) > max_nodes:
                return _result(
                    "council",
                    fallback,
                    [fallback],
                    [],
                    [],
                    f"The requested dependency graph exceeds the configured maximum of {max_nodes} focused Skills.",
                    0.4,
                    True,
                )

            sequential = [target] + tail
            invalid_tail = [
                (sequential[index], sequential[index + 1])
                for index in range(len(sequential) - 1)
                if (sequential[index], sequential[index + 1]) not in declared_handoffs
            ]
            if invalid_tail:
                source, destination = invalid_tail[0]
                return _result(
                    "council",
                    fallback,
                    [fallback],
                    [],
                    [],
                    f"No declared handoff supports {source} -> {destination} after the parallel fan-in; refusing to drop or reorder the requested tail.",
                    0.4,
                    True,
                )

            edges = [[upstream, target] for upstream in pair]
            edges.extend(
                [sequential[index], sequential[index + 1]]
                for index in range(len(sequential) - 1)
            )
            primary = sequential[-1]
            return _result(
                "dag",
                primary,
                nodes,
                edges,
                [list(pair)],
                "The request explicitly declares parallel work, both branches converge through declared handoffs, and every sequential tail transition is declared.",
                0.9,
                False,
            )

        return _result(
            "council",
            fallback,
            [fallback],
            [],
            [],
            "The request asks for parallel work, but no declared parallel-safe handoff graph supports that dependency shape.",
            0.4,
            True,
        )

    if len(requested) > max_nodes:
        return _result(
            "council",
            fallback,
            [fallback],
            [],
            [],
            f"The requested dependency graph exceeds the configured maximum of {max_nodes} focused Skills; refusing to truncate it silently.",
            0.4,
            True,
        )

    if len(requested) < 2:
        skill = requested[0] if requested else ranked[0]
        return _result(
            "focused",
            skill,
            [skill],
            [],
            [],
            "Sequence language was present, but only one focused decision boundary was supported.",
            0.69,
            False,
        )

    invalid_pairs = [
        (requested[index], requested[index + 1])
        for index in range(len(requested) - 1)
        if (requested[index], requested[index + 1]) not in declared_handoffs
    ]
    if invalid_pairs:
        source, target = invalid_pairs[0]
        return _result(
            "council",
            fallback,
            [fallback],
            [],
            [],
            f"No declared handoff supports {source} -> {target}; refusing to reorder or drop explicitly requested Skills.",
            0.4,
            True,
        )

    edges = [[requested[index], requested[index + 1]] for index in range(len(requested) - 1)]
    return _result(
        "dag",
        requested[-1],
        requested,
        edges,
        [],
        "The request explicitly asks for dependent marketing decisions and every transition is supported by a declared handoff.",
        0.84,
        False,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a bounded Marketing Council skill DAG.")
    parser.add_argument("--text", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = route_dynamic(args.text)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else result)


if __name__ == "__main__":
    main()
