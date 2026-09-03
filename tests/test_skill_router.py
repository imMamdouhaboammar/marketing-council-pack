import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "scripts" / "skill_router.py"


class SkillRouterTests(unittest.TestCase):
    def route(self, prompt: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(ROUTER), "--text", prompt, "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_routes_narrow_pricing_request_to_pricing_skill(self):
        payload = self.route("Build a pricing strategy with willingness to pay, price architecture, and discount guardrails")
        self.assertEqual(payload["mode"], "focused")
        self.assertEqual(payload["primary_skill"], "pricing-strategy")

    def test_routes_single_explicit_intent_to_focused_skill(self):
        payload = self.route("Reduce churn")
        self.assertEqual(payload["mode"], "focused")
        self.assertEqual(payload["primary_skill"], "retention-strategy")

    def test_routes_conversion_friction_to_conversion_skill(self):
        payload = self.route("Audit checkout conversion friction and reduce form abandonment without inventing user research")
        self.assertEqual(payload["mode"], "focused")
        self.assertEqual(payload["primary_skill"], "conversion-strategy")

    def test_routes_causal_measurement_to_incrementality(self):
        payload = self.route("Design a geo holdout test to estimate incremental ROAS and reconcile it with attribution")
        self.assertEqual(payload["mode"], "focused")
        self.assertEqual(payload["primary_skill"], "incrementality-design")

    def test_negative_example_blocks_excluded_route(self):
        payload = self.route("Write brand copy without competitor research")
        self.assertNotEqual(payload["primary_skill"], "competitive-intelligence")

    def test_two_distinct_strong_functions_fall_back_to_council(self):
        payload = self.route("Build pricing tiers and discount guardrails while designing a creator commerce program")
        self.assertEqual(payload["mode"], "council")
        self.assertEqual(payload["primary_skill"], "marketing-council")
        self.assertIn("pricing-strategy", payload["secondary_skills"])
        self.assertIn("creator-commerce", payload["secondary_skills"])

    def test_cross_functional_request_falls_back_to_council(self):
        payload = self.route("Create the full go to market strategy including positioning, pricing, campaign, media, retention, and measurement")
        self.assertEqual(payload["mode"], "council")
        self.assertEqual(payload["primary_skill"], "marketing-council")
        self.assertGreaterEqual(len(payload["secondary_skills"]), 2)

    def test_unknown_marketing_request_falls_back_safely(self):
        payload = self.route("Help me make a defensible marketing decision for this messy brief")
        self.assertEqual(payload["mode"], "council")
        self.assertEqual(payload["primary_skill"], "marketing-council")


if __name__ == "__main__":
    unittest.main()
