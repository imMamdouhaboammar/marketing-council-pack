import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "document-registry.json"
VALIDATOR = ROOT / "scripts" / "validate_documentation.py"
ALLOWED = {
    "ACTIVE",
    "ONGOING",
    "HISTORICAL_COMPLETED",
    "HISTORICAL_SUPERSEDED",
    "REFERENCE",
    "DEPRECATED",
}


class DocumentationLifecycleTests(unittest.TestCase):
    def validator_module(self):
        spec = importlib.util.spec_from_file_location("documentation_validator_under_test", VALIDATOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def registry(self):
        self.assertTrue(REGISTRY.is_file(), "docs/document-registry.json must exist")
        return json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_registry_covers_all_markdown_under_docs(self):
        payload = self.registry()
        entries = {item["path"]: item for item in payload["documents"]}
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / "docs").rglob("*.md")
        }
        self.assertEqual(set(entries), actual)
        self.assertEqual(len(entries), len(payload["documents"]))

    def test_registry_status_and_source_of_truth_invariants(self):
        payload = self.registry()
        self.assertEqual(payload["version"], 1)
        for item in payload["documents"]:
            self.assertIn(item["status"], ALLOWED, item["path"])
            self.assertIsInstance(item["source_of_truth"], bool, item["path"])
            self.assertRegex(item["last_reviewed"], r"^2026-09-04$")
            path = ROOT / item["path"]
            self.assertTrue(path.is_file(), item["path"])
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"doc_status: {item['status']}", text, item["path"])
            self.assertIn(
                f"source_of_truth: {str(item['source_of_truth']).lower()}",
                text,
                item["path"],
            )
            if item["status"].startswith("HISTORICAL_"):
                self.assertFalse(item["source_of_truth"], item["path"])
                self.assertIn("Current source of truth", text, item["path"])

    def test_superseded_documents_name_resolving_replacements(self):
        payload = self.registry()
        for item in payload["documents"]:
            if item["status"] != "HISTORICAL_SUPERSEDED":
                continue
            replacements = item.get("superseded_by", [])
            self.assertTrue(replacements, item["path"])
            text = (ROOT / item["path"]).read_text(encoding="utf-8")
            self.assertIn("Do not execute this", text, item["path"])
            for replacement in replacements:
                self.assertTrue((ROOT / replacement).is_file(), replacement)

    def test_ongoing_documents_expose_operational_state(self):
        payload = self.registry()
        required = [
            "Status",
            "Current state",
            "Completed work",
            "Remaining work",
            "Blockers",
            "Next verification step",
            "Source-of-truth references",
            "Last reviewed date",
        ]
        for item in payload["documents"]:
            if item["status"] != "ONGOING":
                continue
            text = (ROOT / item["path"]).read_text(encoding="utf-8")
            for heading in required:
                self.assertIn(heading, text, f"{item['path']}: missing {heading}")

    def test_documentation_index_is_canonical_map(self):
        text = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
        for heading in [
            "Start here",
            "Current product documentation",
            "Ongoing work",
            "Architecture and contracts",
            "Release and distribution",
            "Historical specs",
            "Historical implementation plans",
        ]:
            self.assertIn(heading, text)
        for status in ["ACTIVE", "ONGOING", "HISTORICAL_COMPLETED", "HISTORICAL_SUPERSEDED"]:
            self.assertIn(status, text)

    def test_internal_relative_markdown_links_resolve(self):
        payload = self.registry()
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for item in payload["documents"]:
            path = ROOT / item["path"]
            text = path.read_text(encoding="utf-8")
            for raw in link_re.findall(text):
                target = raw.split("#", 1)[0]
                if not target or "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target).resolve()
                self.assertTrue(
                    resolved.is_file() or resolved.is_dir(),
                    f"{item['path']}: broken relative link {raw}",
                )

    def test_submission_readme_is_ongoing_and_operational(self):
        path = ROOT / "submission" / "README.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("doc_status: ONGOING", text)
        self.assertIn("source_of_truth: false", text)
        for field in [
            "Status",
            "Current state",
            "Completed work",
            "Remaining work",
            "Blockers",
            "Next verification step",
            "Source-of-truth references",
            "Last reviewed date",
        ]:
            self.assertIn(field, text)

    def test_plugin_ci_has_named_documentation_lifecycle_gate(self):
        workflow = (ROOT / ".github" / "workflows" / "plugin-ci.yml").read_text(encoding="utf-8")
        self.assertIn("Validate documentation lifecycle", workflow)
        self.assertIn("python scripts/validate_documentation.py --json", workflow)

    def test_review_dates_are_iso_formatted_and_match_document_metadata_without_fixed_day(self):
        module = self.validator_module()
        self.assertTrue(module.valid_review_date("2027-01-15"))
        self.assertFalse(module.valid_review_date("2027/01/15"))
        metadata = module.parse_document_metadata(
            "<!--\ndoc_status: ACTIVE\nlast_reviewed: 2027-01-15\nsource_of_truth: true\n-->"
        )
        self.assertEqual(metadata["last_reviewed"], "2027-01-15")
        self.assertEqual(
            module.review_date_errors(
                {"path": "docs/example.md", "last_reviewed": "2027-01-15"},
                metadata,
            ),
            [],
        )
        errors = module.review_date_errors(
            {"path": "docs/example.md", "last_reviewed": "2027-01-16"},
            metadata,
        )
        self.assertTrue(any("does not match document metadata" in error for error in errors))

    def test_repo_validator_accepts_documentation_lifecycle(self):
        self.assertTrue(VALIDATOR.is_file(), "scripts/validate_documentation.py must exist")
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"], payload)
        self.assertGreaterEqual(payload["document_count"], 10)


if __name__ == "__main__":
    unittest.main()
