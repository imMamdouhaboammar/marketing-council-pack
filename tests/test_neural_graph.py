import json
import subprocess
import sys
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "neural" / "graph.json"


class NeuralGraphTests(unittest.TestCase):
    def load_graph(self):
        self.assertTrue(GRAPH.exists(), GRAPH)
        return json.loads(GRAPH.read_text(encoding="utf-8"))

    def test_graph_has_expected_node_coverage(self):
        graph = self.load_graph()
        counts = Counter(node["type"] for node in graph["nodes"])
        self.assertGreaterEqual(counts["figure"], 24)
        self.assertGreaterEqual(counts["school"], 12)
        self.assertGreaterEqual(counts["principle"], 24)
        self.assertGreaterEqual(counts["theory"], 16)
        self.assertGreaterEqual(counts["signal"], 14)
        self.assertEqual(counts["agent"], 24)
        self.assertEqual(counts["skill"], 29)
        self.assertGreaterEqual(counts["hook"], 24)

    def test_graph_edges_reference_existing_nodes(self):
        graph = self.load_graph()
        ids = [node["id"] for node in graph["nodes"]]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(ids)
        allowed = {
            "belongs_to", "informs", "operationalizes", "activates", "routes_to",
            "challenges", "counterbalances", "requires", "measured_by", "hands_off_to"
        }
        for edge in graph["edges"]:
            self.assertIn(edge["from"], known, edge)
            self.assertIn(edge["to"], known, edge)
            self.assertIn(edge["relation"], allowed, edge)

    def test_graph_file_nodes_resolve(self):
        graph = self.load_graph()
        for node in graph["nodes"]:
            path = node.get("path")
            if path:
                self.assertTrue((ROOT / path).is_file(), node)

    def test_every_figure_and_theory_is_connected_to_execution(self):
        graph = self.load_graph()
        outgoing = defaultdict(list)
        for edge in graph["edges"]:
            outgoing[edge["from"]].append(edge)
        for node in graph["nodes"]:
            if node["type"] == "figure":
                self.assertTrue(outgoing[node["id"]], node["id"])
            if node["type"] == "theory":
                self.assertTrue(
                    any(edge["relation"] in {"routes_to", "operationalizes", "informs"} for edge in outgoing[node["id"]]),
                    node["id"],
                )

    def test_key_school_counterweights_are_explicit(self):
        graph = self.load_graph()
        pairs = {(e["from"], e["to"]) for e in graph["edges"] if e["relation"] == "counterbalances"}
        required = {
            ("principle-smallest-viable-audience", "principle-penetration-growth"),
            ("principle-performance-accountability", "principle-long-short-horizons"),
            ("principle-positioning-focus", "principle-mental-availability"),
        }
        self.assertTrue(required.issubset(pairs), required - pairs)

    def test_router_returns_expected_specialists(self):
        router = ROOT / "scripts" / "neural_router.py"
        self.assertTrue(router.exists(), router)
        result = subprocess.run(
            [sys.executable, str(router), "--signals", "category-mature,differentiation-weak,competitor-pressure-high", "--json"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("positioning-strategist", payload["agents"])
        self.assertIn("competitive-strategy-analyst", payload["agents"])
        self.assertIn("positioning-strategy", payload["skills"])

    def test_every_agent_skill_and_hook_declares_neural_connections(self):
        for path in (ROOT / "agents").glob("*.md"):
            self.assertIn("## Neural connections", path.read_text(encoding="utf-8"), path)
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertIn("## Neural connections", path.read_text(encoding="utf-8"), path)
        for path in (ROOT / "hooks").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertIn("## Emits", text, path)
            self.assertIn("## Neural connections", text, path)


if __name__ == "__main__":
    unittest.main()
