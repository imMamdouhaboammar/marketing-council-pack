import json
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.unit_economics import calculate_unit_economics
from scripts.funnel_math import calculate_funnel
from scripts.experiment_math import two_proportion_sample_size, summarize_uplift
from scripts.tactic_ranker import rank_tactics
from scripts.strategy_linter import lint_strategy
from scripts.validate_pack import validate_pack


class ScriptTests(unittest.TestCase):
    def test_unit_economics(self):
        r = calculate_unit_economics(
            revenue_per_order=100,
            cogs_per_order=30,
            variable_costs_per_order=10,
            cac=25,
            expected_orders_per_customer=2,
        )
        self.assertEqual(r['contribution_per_order'], 60)
        self.assertEqual(r['customer_contribution_before_acquisition'], 120)
        self.assertEqual(r['net_customer_contribution'], 95)
        self.assertAlmostEqual(r['break_even_roas'], 100 / 60)

    def test_unit_economics_rejects_impossible_inputs(self):
        with self.assertRaises(ValueError):
            calculate_unit_economics(-1, 0, 0, 0, 1)

    def test_funnel_rates(self):
        r = calculate_funnel({'visits': 1000, 'leads': 100, 'customers': 20})
        self.assertAlmostEqual(r['stage_rates']['visits_to_leads'], 0.1)
        self.assertAlmostEqual(r['stage_rates']['leads_to_customers'], 0.2)
        self.assertAlmostEqual(r['overall_conversion'], 0.02)

    def test_funnel_rejects_increasing_counts(self):
        with self.assertRaises(ValueError):
            calculate_funnel({'visits': 100, 'leads': 120})

    def test_experiment_sample_size_and_uplift(self):
        n = two_proportion_sample_size(0.10, 0.02)
        self.assertGreater(n['per_variant'], 1000)
        self.assertEqual(n['total'], n['per_variant'] * 2)
        u = summarize_uplift(0.10, 0.12)
        self.assertAlmostEqual(u['absolute_change'], 0.02)
        self.assertAlmostEqual(u['relative_uplift'], 0.20)

    def test_tactic_ranking_rewards_evidence_and_fit(self):
        tactics = [
            {'name': 'A', 'impact': 8, 'evidence': 9, 'strategic_fit': 9, 'audience_fit': 8,
             'channel_fit': 8, 'measurement': 8, 'speed': 6, 'reversibility': 8, 'cost': 4, 'effort': 4, 'risk': 3},
            {'name': 'B', 'impact': 10, 'evidence': 2, 'strategic_fit': 4, 'audience_fit': 4,
             'channel_fit': 5, 'measurement': 4, 'speed': 8, 'reversibility': 6, 'cost': 5, 'effort': 5, 'risk': 6},
        ]
        ranked = rank_tactics(tactics)
        self.assertEqual(ranked[0]['name'], 'A')
        self.assertGreater(ranked[0]['score'], ranked[1]['score'])

    def test_strategy_linter_finds_generic_and_missing_thresholds(self):
        text = '# Situation\nWe should build awareness and engage the audience.\n# Strategic Choice\nUse social media.\n'
        findings = lint_strategy(text)
        codes = {x['code'] for x in findings}
        self.assertIn('generic-marketing-language', codes)
        self.assertIn('missing-exclusion', codes)
        self.assertIn('missing-thresholds', codes)

    def test_pack_validator_accepts_completed_pack(self):
        result = validate_pack(ROOT)
        self.assertTrue(result['valid'], result['errors'])


if __name__ == '__main__':
    unittest.main()
