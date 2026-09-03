import json
import subprocess
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SkillPackToolingTests(unittest.TestCase):
    def run_script(self,name,*args):
        result=subprocess.run([sys.executable,str(ROOT/"scripts"/name),*args],text=True,capture_output=True); self.assertEqual(result.returncode,0,result.stdout+result.stderr); return json.loads(result.stdout)
    def test_renderer_has_no_committed_drift(self):
        payload=self.run_script("render_skill_packs.py","--check"); self.assertTrue(payload["ok"]); self.assertEqual(payload["files"],261)
    def test_validator_accepts_all_29_full_packs(self):
        payload=self.run_script("validate_skill_packs.py"); self.assertTrue(payload["ok"]); self.assertEqual(payload["skills"],29)
    def test_bineval_scores_every_pack_at_full_structural_coverage(self):
        payload=self.run_script("skill_bineval.py","--json"); self.assertTrue(payload["ok"]); self.assertEqual(payload["skills"],29); self.assertEqual(payload["minimum_score"],100)
    def test_evidence_ledger_is_complete(self):
        payload=self.run_script("evidence_ledger.py"); self.assertTrue(payload["ok"]); self.assertEqual(payload["skills"],29)
if __name__=="__main__": unittest.main()
