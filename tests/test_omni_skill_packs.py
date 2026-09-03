import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES = json.loads((ROOT / "routing" / "skill-routes.json").read_text(encoding="utf-8"))
FOCUSED = [route["skill"] for route in ROUTES["routes"]]
ALL_SKILLS = sorted(FOCUSED + [ROUTES["fallback_skill"]])

REQUIRED_LOCAL_FILES = (
    "references/skill-spec.json",
    "references/decision-model.md",
    "references/failure-modes.md",
    "references/output-contract.md",
    "evals/activation.yml",
    "evals/behavior.yml",
    "evals/pressure.yml",
    "evals/regression.yml",
)

REQUIRED_SPEC_FIELDS = (
    "name",
    "purpose",
    "baseline_failures",
    "activation",
    "outputs",
    "invariants",
    "non_goals",
    "workflow",
    "capabilities",
    "evidence_policy",
    "failure_behavior",
    "completion_conditions",
    "handoffs",
    "host_targets",
    "eval_files",
)


def load_spec(slug):
    path = ROOT / "skills" / slug / "references" / "skill-spec.json"
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def yaml_case_count(path):
    if not path.is_file():
        return 0
    return len(re.findall(r"^- id:\s*[a-z0-9-]+\s*$", path.read_text(encoding="utf-8"), flags=re.M))


class OmniSkillPackTests(unittest.TestCase):
    def test_inventory_is_29_total_and_28_focused(self):
        self.assertEqual(len(FOCUSED), 28)
        self.assertEqual(len(set(FOCUSED)), 28)
        self.assertEqual(len(ALL_SKILLS), 29)

    def test_every_skill_is_a_full_pack(self):
        for slug in ALL_SKILLS:
            root = ROOT / "skills" / slug
            self.assertTrue((root / "SKILL.md").is_file(), slug)
            self.assertTrue((root / "agents" / "openai.yaml").is_file(), slug)
            for rel in REQUIRED_LOCAL_FILES:
                self.assertTrue((root / rel).is_file(), f"{slug}: missing {rel}")

    def test_every_skill_spec_has_complete_behavioral_contract(self):
        valid_freedom = {"low", "medium", "high"}
        for slug in ALL_SKILLS:
            spec = load_spec(slug)
            self.assertIsNotNone(spec, f"{slug}: missing skill-spec.json")
            for field in REQUIRED_SPEC_FIELDS:
                self.assertIn(field, spec, f"{slug}: missing spec field {field}")
            self.assertEqual(spec["name"], slug)
            self.assertGreaterEqual(len(spec["baseline_failures"]), 3, slug)
            activation = spec["activation"]
            self.assertGreaterEqual(len(activation.get("positive", [])), 3, slug)
            self.assertGreaterEqual(len(activation.get("implicit", [])), 3, slug)
            self.assertGreaterEqual(len(activation.get("negative", [])), 2, slug)
            self.assertGreaterEqual(len(activation.get("collisions", [])), 1, slug)
            self.assertGreaterEqual(len(spec["outputs"]), 3, slug)
            self.assertGreaterEqual(len(spec["invariants"]), 3, slug)
            self.assertGreaterEqual(len(spec["workflow"]), 4, slug)
            self.assertTrue(spec["completion_conditions"], slug)
            self.assertTrue(spec["failure_behavior"], slug)
            self.assertIn("required", spec["capabilities"], slug)
            self.assertIn("optional", spec["capabilities"], slug)
            self.assertIn("not_allowed", spec["capabilities"], slug)
            for step in spec["workflow"]:
                for field in ("id", "action", "why", "freedom", "evidence_required", "completion"):
                    self.assertTrue(step.get(field), f"{slug}: workflow step missing {field}")
                self.assertIn(step["freedom"], valid_freedom, f"{slug}: invalid freedom")

    def test_focused_specs_are_not_template_clones(self):
        failure_fingerprints = {}
        workflow_fingerprints = {}
        for slug in FOCUSED:
            spec = load_spec(slug)
            self.assertIsNotNone(spec, slug)
            failure_fp = tuple(item.strip().lower() for item in spec["baseline_failures"])
            workflow_fp = tuple(step["action"].strip().lower() for step in spec["workflow"])
            self.assertNotIn(failure_fp, failure_fingerprints, f"{slug}: cloned failures from {failure_fingerprints.get(failure_fp)}")
            self.assertNotIn(workflow_fp, workflow_fingerprints, f"{slug}: cloned workflow from {workflow_fingerprints.get(workflow_fp)}")
            failure_fingerprints[failure_fp] = slug
            workflow_fingerprints[workflow_fp] = slug

    def test_local_eval_suites_meet_minimum_behavioral_coverage(self):
        minimums = {
            "activation.yml": 9,
            "behavior.yml": 3,
            "pressure.yml": 2,
            "regression.yml": 1,
        }
        for slug in ALL_SKILLS:
            eval_dir = ROOT / "skills" / slug / "evals"
            for filename, minimum in minimums.items():
                self.assertGreaterEqual(
                    yaml_case_count(eval_dir / filename),
                    minimum,
                    f"{slug}: {filename} needs >= {minimum} cases",
                )

    def test_skill_md_is_progressive_disclosure_map(self):
        required_pointers = (
            "references/skill-spec.json",
            "references/decision-model.md",
            "references/failure-modes.md",
            "references/output-contract.md",
        )
        for slug in ALL_SKILLS:
            text = (ROOT / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
            self.assertLess(len(text.splitlines()), 220, f"{slug}: SKILL.md should be a map, not the full manual")
            for pointer in required_pointers:
                self.assertIn(pointer, text, f"{slug}: missing point-of-use pointer {pointer}")
            self.assertRegex(text, r"(?i)completion|complete when|completion gate", f"{slug}: missing completion gate")
            self.assertRegex(text, r"(?i)evidence", f"{slug}: missing evidence discipline")

    def test_declared_eval_files_exist(self):
        for slug in ALL_SKILLS:
            spec = load_spec(slug)
            self.assertIsNotNone(spec, slug)
            declared = spec["eval_files"]
            self.assertEqual(len(declared), 4, slug)
            for rel in declared:
                self.assertTrue((ROOT / "skills" / slug / rel).is_file(), f"{slug}: missing declared eval {rel}")

    def test_skill_packs_do_not_contain_private_paths_or_secret_shapes(self):
        forbidden = ("/Users/", "/home/", "sk-proj-", "BEGIN PRIVATE KEY")
        for slug in ALL_SKILLS:
            root = ROOT / "skills" / slug
            for path in root.rglob("*"):
                if not path.is_file() or path.suffix not in {".md", ".json", ".yml", ".yaml", ".py"}:
                    continue
                text = path.read_text(encoding="utf-8")
                for token in forbidden:
                    self.assertNotIn(token, text, f"{path}: forbidden private/secret-shaped content")

    def test_standalone_openai_bundles_carry_local_contracts_and_evals(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "submission"
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_openai_submission_pack.py"),
                    "--output-root",
                    str(out),
                    "--json",
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["skill_bundle_count"], 29)
            inventory = json.loads((out / "submission-inventory.json").read_text(encoding="utf-8"))
            for item in inventory["skills"]:
                slug = item["name"]
                archive = out / item["archive"]
                self.assertTrue(archive.is_file(), slug)
                with zipfile.ZipFile(archive) as zf:
                    names = set(zf.namelist())
                for rel in REQUIRED_LOCAL_FILES:
                    self.assertIn(f"{slug}/{rel}", names, f"{slug}: standalone bundle missing {rel}")


if __name__ == "__main__":
    unittest.main()
