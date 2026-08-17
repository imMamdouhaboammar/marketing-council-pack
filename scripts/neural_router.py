#!/usr/bin/env python3
"""Rank Marketing Council nodes from normalized diagnostic signals."""
from __future__ import annotations
import argparse, json
from collections import defaultdict, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "neural" / "graph.json"
FOLLOW = {"activates", "informs", "operationalizes", "routes_to", "challenges", "counterbalances", "hands_off_to"}


def route(signals: list[str]) -> dict:
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    outgoing = defaultdict(list)
    for e in graph["edges"]:
        outgoing[e["from"]].append(e)
    scores = defaultdict(float)
    reasons = defaultdict(set)
    queue = deque()
    for raw in signals:
        raw = raw.strip()
        if not raw:
            continue
        nid = raw if raw.startswith("signal-") else f"signal-{raw}"
        if nid not in nodes:
            continue
        queue.append((nid, 0, raw))
        scores[nid] += 10
    seen_depth = {}
    while queue:
        current, depth, origin = queue.popleft()
        if depth >= 3:
            continue
        for e in outgoing.get(current, []):
            if e["relation"] not in FOLLOW:
                continue
            target = e["to"]
            step = float(e.get("weight", 1)) * (3 - depth)
            scores[target] += step
            reasons[target].add(origin)
            key = (target, origin)
            next_depth = depth + 1
            if seen_depth.get(key, 99) > next_depth:
                seen_depth[key] = next_depth
                queue.append((target, next_depth, origin))

    def ranked(node_type: str, limit: int = 8) -> list[str]:
        items = [(score, nid) for nid, score in scores.items() if nodes.get(nid, {}).get("type") == node_type]
        items.sort(key=lambda x: (-x[0], x[1]))
        return [nodes[nid].get("slug", nid) for _, nid in items[:limit]]

    return {
        "signals": [s for s in signals if (s if s.startswith("signal-") else f"signal-{s}") in nodes],
        "agents": ranked("agent"),
        "skills": ranked("skill"),
        "theories": ranked("theory"),
        "principles": ranked("principle"),
        "hooks": ranked("hook"),
        "schools": ranked("school"),
        "figures": ranked("figure"),
        "evidence": ranked("evidence"),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--signals", required=True, help="Comma-separated normalized signal IDs")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    result = route([s.strip() for s in args.signals.split(",") if s.strip()])
    print(json.dumps(result, indent=2) if args.json else "\n".join(f"{k}: {', '.join(v)}" for k, v in result.items()))


if __name__ == "__main__":
    main()
