import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "scripts" / "dynamic_router.py"


class DynamicRouterTests(unittest.TestCase):
    def _module(self):
        self.assertTrue(ROUTER_PATH.is_file(), "scripts/dynamic_router.py must exist")
        spec = importlib.util.spec_from_file_location("dynamic_router_under_test", ROUTER_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _route(self, text):
        module = self._module()
        result = module.route_dynamic(text)
        self.assertIn(result["mode"], {"focused", "council", "dag"})
        self.assertIn("primary_skill", result)
        self.assertIn("nodes", result)
        self.assertIn("edges", result)
        self.assertIn("parallel_groups", result)
        self.assertIn("confidence", result)
        self.assertIn("reason", result)
        self.assertIn("fallback", result)
        return result

    def test_single_dominant_function_stays_focused(self):
        result = self._route("Set pricing tiers and discount guardrails for our subscription")
        self.assertEqual(result["mode"], "focused")
        self.assertEqual(result["primary_skill"], "pricing-strategy")
        self.assertEqual(result["nodes"], ["pricing-strategy"])
        self.assertEqual(result["edges"], [])

    def test_ambiguous_cross_functional_problem_falls_back_to_council(self):
        result = self._route("Growth is weak and we do not know whether the issue is positioning pricing media or retention. Diagnose what matters first")
        self.assertEqual(result["mode"], "council")
        self.assertEqual(result["primary_skill"], "marketing-council")
        self.assertTrue(result["fallback"])

    def test_explicit_dependency_chain_builds_ordered_dag(self):
        result = self._route("First diagnose the market, then choose target segments, position the product, set pricing tiers, and build the go-to-market launch sequence")
        self.assertEqual(result["mode"], "dag")
        expected = [
            "market-diagnosis",
            "segmentation-strategy",
            "positioning-strategy",
            "pricing-strategy",
            "go-to-market",
        ]
        self.assertEqual(result["nodes"], expected)
        self.assertIn(["market-diagnosis", "segmentation-strategy"], result["edges"])
        self.assertIn(["segmentation-strategy", "positioning-strategy"], result["edges"])
        self.assertIn(["positioning-strategy", "pricing-strategy"], result["edges"])
        self.assertIn(["pricing-strategy", "go-to-market"], result["edges"])

    def test_independent_research_can_run_in_parallel_before_positioning(self):
        result = self._route("Research customer switching triggers and competitor alternatives in parallel, then decide our positioning")
        self.assertEqual(result["mode"], "dag")
        self.assertEqual(result["primary_skill"], "positioning-strategy")
        self.assertIn(["customer-research", "competitive-intelligence"], result["parallel_groups"])
        self.assertIn(["customer-research", "positioning-strategy"], result["edges"])
        self.assertIn(["competitive-intelligence", "positioning-strategy"], result["edges"])

    def test_unordered_collision_does_not_invent_a_dag(self):
        result = self._route("Conversion and retention are both down but instrumentation is incomplete and we cannot tell which problem is primary")
        self.assertEqual(result["mode"], "council")
        self.assertEqual(result["primary_skill"], "marketing-council")

    def test_graph_is_bounded_to_six_focused_nodes(self):
        result = self._route(
            "Diagnose the market, research customers, map competitors, segment the market, position the product, set pricing, build GTM, campaign, media, content, conversion and retention plans"
        )
        self.assertLessEqual(len(result["nodes"]), 6)

    def test_dynamic_router_does_not_return_neural_theory_nodes(self):
        result = self._route("Research customers and competitors, then decide positioning")
        for node in result["nodes"]:
            self.assertNotIn("theory", node.lower())
            self.assertNotIn("principle", node.lower())
            self.assertNotIn("agent", node.lower())


if __name__ == "__main__":
    unittest.main()
