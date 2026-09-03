import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillPackToolingTests(unittest.TestCase):
    def run_script(self, name, *args):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / name), *args],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_renderer_has_no_committed_drift(self):
        payload = self.run_script("render_skill_packs.py", "--check")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["files"], 261)

    def test_validator_accepts_all_29_full_packs(self):
        payload = self.run_script("validate_skill_packs.py")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["skills"], 29)

    def test_bineval_scores_every_pack_at_full_structural_coverage(self):
        payload = self.run_script("skill_bineval.py", "--json")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["skills"], 29)
        self.assertEqual(payload["minimum_score"], 100)

    def test_evidence_ledger_is_complete(self):
        payload = self.run_script("evidence_ledger.py")
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["skills"], 29)

    def test_execution_bindings_cover_every_focused_skill_and_resolve(self):
        bindings_path = ROOT / "routing" / "skill-execution-bindings.json"
        self.assertTrue(bindings_path.is_file(), bindings_path)
        bindings = json.loads(bindings_path.read_text(encoding="utf-8"))["bindings"]
        focused = {
            path.parent.name
            for path in (ROOT / "skills").glob("*/SKILL.md")
            if path.parent.name != "marketing-council"
        }
        self.assertEqual(set(bindings), focused)
        for slug, binding in bindings.items():
            self.assertTrue((ROOT / "agents" / f"{binding['primary_agent']}.md").is_file(), slug)
            self.assertTrue((ROOT / "agents" / f"{binding['counterweight_agent']}.md").is_file(), slug)
            self.assertTrue((ROOT / "hooks" / f"{binding['primary_hook']}.md").is_file(), slug)
            self.assertTrue((ROOT / "hooks" / "evidence-gate.md").is_file(), slug)


if __name__ == "__main__":
    unittest.main()
