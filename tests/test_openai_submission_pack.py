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


if __name__ == "__main__":
    unittest.main()
