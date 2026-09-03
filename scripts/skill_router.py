#!/usr/bin/env python3
"""Deterministically route a marketing request to one focused skill or the council.

The router is intentionally conservative. It selects a focused skill only when
one function clearly owns the request. Explicit registry negative examples
exclude a route, while ambiguous and cross-functional briefs fall back to
Marketing Council.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "routing" / "skill-routes.json"
CROSS_FUNCTIONAL_MARKERS = {
    "positioning",
    "pricing",
    "campaign",
    "media",
    "retention",
    "measurement",
    "brand",
    "content",
    "conversion",
    "segmentation",
    "category",
    "offer",
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = value.replace("–", "-").replace("—", "-")
    value = re.sub(r"[^a-z0-9+/#.\-\s]", " ", value)
    value = value.replace("-", " ")
    return " ".join(value.split())


def phrase_score(text: str, phrase: str) -> int:
    phrase = normalize(phrase)
    if not phrase:
        return 0
    if phrase in text:
        words = phrase.split()
        # A single exact intent must be strong enough to own a narrow request.
        return 7 + min(len(words), 4)
    tokens = [token for token in phrase.split() if len(token) >= 3]
    if not tokens:
        return 0
    hits = sum(1 for token in tokens if re.search(rf"\b{re.escape(token)}\b", text))
    if hits == len(tokens) and hits >= 2:
        return hits
    return 0


def load_registry() -> dict:
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def explicit_domain_markers(text: str) -> list[str]:
    return sorted(
        marker
        for marker in CROSS_FUNCTIONAL_MARKERS
        if re.search(rf"\b{re.escape(marker)}\b", text)
    )


def route_is_excluded(text: str, item: dict) -> bool:
    """Treat a matched negative example as a hard boundary for that route."""
    for example in item.get("negative_examples", []):
        normalized_example = normalize(example)
        if normalized_example and normalized_example in text:
            return True
        if phrase_score(text, example) >= 8:
            return True
    return False


def council_result(fallback: str, secondaries: list[str], confidence: float, reason: str) -> dict:
    return {
        "mode": "council",
        "primary_skill": fallback,
        "selected_skill": fallback,
        "fallback": True,
        "secondary_skills": secondaries,
        "confidence": round(confidence, 3),
        "reason": reason,
    }


def focused_result(skill: str, secondaries: list[str], confidence: float) -> dict:
    return {
        "mode": "focused",
        "primary_skill": skill,
        "selected_skill": skill,
        "fallback": False,
        "secondary_skills": secondaries,
        "confidence": round(confidence, 3),
        "reason": "One focused skill clearly owns the next marketing decision.",
    }


def route(text: str) -> dict:
    registry = load_registry()
    normalized = normalize(text)
    scored: list[dict] = []

    for item in registry["routes"]:
        if route_is_excluded(normalized, item):
            continue
        score = sum(phrase_score(normalized, phrase) for phrase in item["intents"])
        if score:
            scored.append({
                "skill": item["skill"],
                "score": score,
                "priority": item.get("priority", 0),
            })

    scored.sort(key=lambda item: (item["score"], item["priority"], item["skill"]), reverse=True)
    fallback = registry["fallback_skill"]
    domain_markers = explicit_domain_markers(normalized)

    if not scored:
        return council_result(
            fallback,
            [],
            0.0,
            "No focused route had enough explicit evidence.",
        )

    strong = [item for item in scored if item["score"] >= 8]
    top = scored[0]
    second = scored[1] if len(scored) > 1 else None

    # Two independently strong functions are already cross-functional.
    cross_functional = len(strong) >= 2 or len(domain_markers) >= 3
    ambiguous = bool(second and second["score"] >= 8 and top["score"] - second["score"] <= 3)
    focused = top["score"] >= 8 and not cross_functional and not ambiguous

    max_secondary = registry.get("routing_policy", {}).get("max_secondary_skills", 5)
    secondaries = [item["skill"] for item in scored[:max_secondary]]

    if not focused:
        confidence = min(0.79, top["score"] / max(1, top["score"] + sum(i["score"] for i in scored[1:3])))
        return council_result(
            fallback,
            secondaries,
            confidence,
            "Multiple plausible functions are active or no route clearly dominates.",
        )

    denominator = top["score"] + (second["score"] if second else 0)
    confidence = top["score"] / denominator if denominator else 1.0
    return focused_result(
        top["skill"],
        [item["skill"] for item in scored[1:3] if item["score"] >= 4],
        confidence,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a marketing request to Marketing Council skills.")
    parser.add_argument("--text", required=True, help="Marketing request to classify")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    result = route(args.text)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(result["primary_skill"])


if __name__ == "__main__":
    main()
