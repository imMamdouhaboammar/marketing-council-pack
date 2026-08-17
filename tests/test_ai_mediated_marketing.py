import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_AGENTS = {
    "ai-discovery-strategist",
    "agentic-commerce-strategist",
    "marketing-automation-governor",
    "marketing-signal-architect",
    "creator-commerce-strategist",
    "commerce-media-strategist",
}
NEW_SKILLS = {
    "ai-discovery-strategy",
    "conversational-advertising",
    "agentic-commerce",
    "commerce-feed-intelligence",
    "autonomous-media-operations",
    "marketing-signal-strategy",
    "incrementality-design",
    "creator-commerce",
    "commerce-media-strategy",
}
NEW_HOOKS = {
    "ai-surface-check",
    "agentic-commerce-readiness",
    "commerce-feed-readiness",
    "marketing-signal-quality",
    "automation-authority-check",
    "automation-black-box-check",
    "incrementality-required",
    "creative-provenance-check",
    "creator-measurement-check",
    "closed-loop-bias-check",
}
NEW_SCHOOLS = {
    "ai-mediated-discovery",
    "agentic-commerce",
    "autonomous-marketing-operations",
    "causal-measurement",
    "creator-commerce",
}
NEW_SIGNALS = {
    "ai-discovery-dominant",
    "conversational-intent-high",
    "answer-surface-visibility-low",
    "agentic-checkout-available",
    "product-feed-poor",
    "product-data-rich",
    "platform-automation-high",
    "manual-control-low",
    "automation-boundaries-unclear",
    "crm-signal-rich",
    "crm-signal-poor",
    "outcome-delay-high",
    "attribution-fragmented",
    "incrementality-unknown",
    "creator-led-discovery",
    "creator-measurement-fragmented",
    "commerce-media-available",
    "closed-loop-data-available",
    "commerce-media-bias-risk",
    "synthetic-creative-scale",
    "provenance-sensitive",
}


class AIMediatedMarketingTests(unittest.TestCase):
    def load_graph(self):
        return json.loads((ROOT / "neural" / "graph.json").read_text(encoding="utf-8"))

    def test_release_and_component_targets(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.3.0")
        self.assertEqual(len(list((ROOT / "agents").glob("*.md"))), 24)
        self.assertEqual(len([p for p in (ROOT / "skills").iterdir() if p.is_dir()]), 29)
        self.assertEqual(len(list((ROOT / "hooks").glob("*.md"))), 24)

    def test_required_v13_components_exist(self):
        self.assertTrue(NEW_AGENTS.issubset({p.stem for p in (ROOT / "agents").glob("*.md")}))
        self.assertTrue(NEW_SKILLS.issubset({p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}))
        self.assertTrue(NEW_HOOKS.issubset({p.stem for p in (ROOT / "hooks").glob("*.md")}))
        self.assertTrue(NEW_SCHOOLS.issubset({p.stem for p in (ROOT / "references" / "schools").glob("*.md")}))

    def test_graph_contains_2026_signals_and_evidence(self):
        graph = self.load_graph()
        nodes = {n["id"]: n for n in graph["nodes"]}
        for signal in NEW_SIGNALS:
            self.assertIn(f"signal-{signal}", nodes)
        evidence = [n for n in graph["nodes"] if n["type"] == "evidence"]
        self.assertGreaterEqual(len(evidence), 6)
        for node in evidence:
            self.assertRegex(node.get("as_of", ""), r"^2026-")
            self.assertTrue(node.get("source_ids"), node)
            self.assertTrue((ROOT / node["path"]).is_file(), node)

    def test_router_handles_ai_discovery_and_agentic_commerce(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "neural_router.py"), "--signals",
             "ai-discovery-dominant,conversational-intent-high,product-feed-poor,agentic-checkout-available", "--json"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("ai-discovery-strategist", payload["agents"])
        self.assertIn("agentic-commerce-strategist", payload["agents"])
        self.assertIn("ai-discovery-strategy", payload["skills"])
        self.assertIn("commerce-feed-intelligence", payload["skills"])
        self.assertIn("agentic-commerce", payload["skills"])

    def test_router_handles_autonomous_media_and_measurement(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "neural_router.py"), "--signals",
             "platform-automation-high,automation-boundaries-unclear,crm-signal-poor,incrementality-unknown", "--json"],
            text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("marketing-automation-governor", payload["agents"])
        self.assertIn("marketing-signal-architect", payload["agents"])
        self.assertIn("autonomous-media-operations", payload["skills"])
        self.assertIn("marketing-signal-strategy", payload["skills"])
        self.assertIn("incrementality-design", payload["skills"])

    def test_2026_sources_are_registered(self):
        registry = (ROOT / "references" / "sources.yml").read_text(encoding="utf-8")
        required = {
            "google-search-ai-owner-controls-2026",
            "google-gml-search-ads-2026",
            "google-agentic-commerce-2026",
            "google-ask-advisor-2026",
            "google-meridian-ga360-2026",
            "tiktok-world-2026",
            "tiktok-symphony-agent-2026",
            "meta-ai-ads-2026",
            "iab-state-data-2026",
            "iab-creator-measurement-2026",
            "iab-commerce-media-2026",
        }
        for source_id in required:
            self.assertIn(f"  {source_id}:", registry)

    def test_public_components_keep_neural_contracts(self):
        for name in NEW_AGENTS:
            self.assertIn("## Neural connections", (ROOT / "agents" / f"{name}.md").read_text(encoding="utf-8"))
        for name in NEW_SKILLS:
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Neural connections", text)
            self.assertIn('version: "1.3.0"', text)
        for name in NEW_HOOKS:
            text = (ROOT / "hooks" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("## Emits", text)
            self.assertIn("## Neural connections", text)


if __name__ == "__main__":
    unittest.main()
