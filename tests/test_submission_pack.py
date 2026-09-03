import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "submission" / "submission-pack.json"
VALIDATOR = ROOT / "scripts" / "validate_submission_pack.py"


class SubmissionPackTests(unittest.TestCase):
    def load(self):
        self.assertTrue(PACK.is_file(), "submission/submission-pack.json must exist")
        return json.loads(PACK.read_text(encoding="utf-8"))

    def test_pack_is_skills_only_v1_5_and_truthful_about_portal_state(self):
        pack = self.load()
        self.assertEqual(pack["schema_version"], 1)
        self.assertEqual(pack["artifact_use"], "SUBMISSION_DRAFT")
        self.assertEqual(pack["pack_status"], "PARTIAL_MISSING_INPUT")
        self.assertEqual(pack["submission_type"], "skills-only")
        self.assertEqual(pack["plugin"]["version"], "1.5.0")
        self.assertEqual(pack["plugin"]["skill_count"], 29)
        self.assertEqual(pack["plugin"]["focused_skill_count"], 28)
        self.assertFalse(pack["portal_state"]["submitted"])
        self.assertFalse(pack["portal_state"]["reviewed"])
        self.assertFalse(pack["portal_state"]["approved"])
        self.assertFalse(pack["portal_state"]["published"])

    def test_pack_has_exactly_five_positive_and_three_negative_evidence_cases(self):
        pack = self.load()
        cases = pack["review_cases"]
        positive = [case for case in cases if case["kind"] == "positive"]
        negative = [case for case in cases if case["kind"] == "negative"]
        self.assertEqual(len(positive), 5)
        self.assertEqual(len(negative), 3)
        self.assertEqual(len(cases), 8)
        for case in cases:
            self.assertEqual(case["evidence_kind"], "PASSED_TEST_EVIDENCE")
            self.assertTrue(case["prompt"])
            self.assertTrue(case["expected_behavior"])
            self.assertTrue(case["expected_result_shape"])
            self.assertTrue(case["actual_result_summary"])
            self.assertRegex(case["evidence_reference"], r"^tests/test_(skill|dynamic)_router\.py::test_")

    def test_pack_does_not_hide_required_external_submission_gaps(self):
        pack = self.load()
        missing = set(pack["missing_required_inputs"])
        self.assertEqual(
            missing,
            {
                "verified_developer_identity",
                "privacy_policy_url",
                "terms_of_service_url",
                "support_url",
                "country_or_region_availability",
            },
        )
        self.assertIn("public ChatGPT/Codex publication", pack["release_boundary"])
        self.assertIn("not performed", pack["release_boundary"])

    def test_repo_validator_accepts_current_submission_draft(self):
        self.assertTrue(VALIDATOR.is_file(), "scripts/validate_submission_pack.py must exist")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), str(PACK), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"], payload)
        self.assertEqual(payload["positive_cases"], 5)
        self.assertEqual(payload["negative_cases"], 3)
        self.assertEqual(payload["pack_status"], "PARTIAL_MISSING_INPUT")

    def test_release_notes_include_late_router_and_symlink_hardening(self):
        pack = self.load()
        notes = pack["release_notes"]
        self.assertIn("declared handoff", notes)
        self.assertIn("symlink", notes)
        self.assertIn("29", notes)


if __name__ == "__main__":
    unittest.main()
