import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDER = ROOT / "scripts" / "build_openai_submission_pack.py"


class OpenAISubmissionPackTests(unittest.TestCase):
    def module(self):
        scripts = str(ROOT / "scripts")
        sys.path.insert(0, scripts)
        try:
            spec = importlib.util.spec_from_file_location("openai_submission_builder_under_test", BUILDER)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        finally:
            sys.path.remove(scripts)

    def build(self, output: Path) -> dict:
        result = subprocess.run(
            [sys.executable, str(BUILDER), "--output-root", str(output), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_marketing_council_bundle_contains_all_focused_skill_modules(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td)
            self.build(output)
            archive = output / "skills" / "marketing-council-v1.5.0.zip"
            self.assertTrue(archive.exists(), archive)
            with zipfile.ZipFile(archive) as zf:
                names = set(zf.namelist())
                focused = {
                    path.parent.name
                    for path in (ROOT / "skills").glob("*/SKILL.md")
                    if path.parent.name != "marketing-council"
                }
                packaged = {
                    name.split("/")[2]
                    for name in names
                    if name.startswith("marketing-council/skills/") and name.endswith("/SKILL.md")
                }
                self.assertEqual(packaged, focused)

                council_text = zf.read("marketing-council/SKILL.md").decode("utf-8")
                self.assertNotIn("load a focused sibling skill", council_text)
                self.assertNotIn("load the matching focused skill under `../`", council_text)
                self.assertIn("skills/", council_text)

                for slug in sorted(focused):
                    nested = zf.read(f"marketing-council/skills/{slug}/SKILL.md").decode("utf-8")
                    self.assertNotIn("../../agents/", nested, slug)
                    self.assertNotIn("../../hooks/", nested, slug)
                    self.assertIn("../../shared/agents/", nested, slug)
                    self.assertIn("../../shared/hooks/", nested, slug)

                archive_names = "\n".join(sorted(names))
                self.assertIn("marketing-council/shared/agents/", archive_names)
                self.assertIn("marketing-council/shared/hooks/", archive_names)

    def test_rebuild_removes_stale_generated_archives(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td)
            self.build(output)
            stale_skill = output / "skills" / "removed-skill-v0.0.0.zip"
            stale_plugin = output / "plugin" / "old-plugin-v0.0.0.zip"
            stale_skill.write_bytes(b"stale")
            stale_plugin.write_bytes(b"stale")

            payload = self.build(output)
            self.assertFalse(stale_skill.exists())
            self.assertFalse(stale_plugin.exists())
            self.assertEqual(payload["skill_bundle_count"], 29)
            self.assertEqual(len(list((output / "skills").glob("*.zip"))), 29)


    def test_standalone_skill_specs_resolve_bundle_local_execution_paths(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "submission"
            self.build(output)

            pricing_archive = output / "skills" / "pricing-strategy-v1.5.0.zip"
            with zipfile.ZipFile(pricing_archive) as zf:
                spec = json.loads(zf.read("pricing-strategy/references/skill-spec.json"))
            self.assertEqual(
                spec["execution"]["binding_source"],
                "../shared/routing/skill-execution-bindings.json",
            )
            self.assertEqual(spec["handoffs"]["dynamic_router"], "../shared/scripts/dynamic_router.py")
            self.assertEqual(spec["handoffs"]["skill_router"], "../shared/scripts/skill_router.py")
            self.assertEqual(spec["handoffs"]["neural_router"], "../shared/scripts/neural_router.py")

            council_archive = output / "skills" / "marketing-council-v1.5.0.zip"
            with zipfile.ZipFile(council_archive) as zf:
                nested = json.loads(
                    zf.read("marketing-council/skills/pricing-strategy/references/skill-spec.json")
                )
            self.assertEqual(
                nested["execution"]["binding_source"],
                "../../../shared/routing/skill-execution-bindings.json",
            )
            self.assertEqual(
                nested["handoffs"]["dynamic_router"],
                "../../../shared/scripts/dynamic_router.py",
            )
            self.assertEqual(nested["handoffs"]["skill_router"], "../../../shared/scripts/skill_router.py")
            self.assertEqual(nested["handoffs"]["neural_router"], "../../../shared/scripts/neural_router.py")

    def test_shared_markdown_paths_are_rewritten_to_bundle_local_resources(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "submission"
            self.build(output)
            archive = output / "skills" / "agentic-commerce-v1.5.0.zip"
            with zipfile.ZipFile(archive) as zf:
                theory = zf.read(
                    "agentic-commerce/shared/references/theories/agentic-commerce-readiness.md"
                ).decode("utf-8")
                hook = zf.read(
                    "agentic-commerce/shared/hooks/agentic-commerce-readiness.md"
                ).decode("utf-8")
            self.assertIn("shared/neural/graph.json", theory)
            self.assertIn("shared/references/2026/agentic-commerce-2026.md", theory)
            self.assertNotIn("`neural/graph.json`", theory)
            self.assertNotIn("`references/2026/agentic-commerce-2026.md`", theory)
            self.assertIn("shared/references/2026/", hook)

    def test_builder_rejects_root_level_symlink_source(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            skill = root / "sample-skill"
            (skill / "agents").mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: sample-skill\ndescription: Sample skill\n---\nBody\n", encoding="utf-8")
            (skill / "agents" / "openai.yaml").write_text("interface:\n  display_name: Sample\n", encoding="utf-8")
            outside = root / "outside.txt"
            outside.write_text("must not be packaged", encoding="utf-8")
            (skill / "leak.txt").symlink_to(outside)

            with self.assertRaises(ValueError):
                module.build_skill_bundle(skill, root / "out", "1.5.0")

    def test_copy_helpers_reject_nested_symlink_sources(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root / "outside.txt"
            outside.write_text("must not be packaged", encoding="utf-8")

            clean_src = root / "clean-src"
            clean_src.mkdir()
            (clean_src / "nested-link.txt").symlink_to(outside)
            with self.assertRaises(ValueError):
                module.copy_clean(clean_src, root / "clean-dst")

            focused_src = root / "focused-src"
            focused_src.mkdir()
            (focused_src / "SKILL.md").write_text("---\nname: focused\ndescription: Focused\n---\nBody\n", encoding="utf-8")
            (focused_src / "nested-link.txt").symlink_to(outside)
            with self.assertRaises(ValueError):
                module.copy_focused_module(focused_src, root / "focused-dst")

    def test_deterministic_zip_rejects_symlink_members(self):
        module = self.module()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            source.mkdir()
            outside = root / "outside.txt"
            outside.write_text("must not be packaged", encoding="utf-8")
            (source / "leak.txt").symlink_to(outside)
            with self.assertRaises(ValueError):
                module.deterministic_zip(source, root / "archive.zip", "sample")



if __name__ == "__main__":
    unittest.main()
