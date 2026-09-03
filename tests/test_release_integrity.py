import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseIntegrityTests(unittest.TestCase):
    def current_version(self) -> str:
        return json.loads(
            (ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )["version"]

    def previous_minor_version(self, version: str) -> str | None:
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", version)
        self.assertIsNotNone(match, version)
        major, minor, patch = (int(part) for part in match.groups())
        if patch > 0:
            return f"{major}.{minor}.{patch - 1}"
        if minor > 0:
            return f"{major}.{minor - 1}.0"
        return None

    def test_public_manifests_share_current_version(self):
        expected = self.current_version()
        manifests = [
            ROOT / "manifest.json",
            ROOT / ".codex-plugin" / "plugin.json",
            ROOT / ".claude-plugin" / "plugin.json",
            ROOT / ".claude-plugin" / "marketplace.json",
            ROOT / "submission" / "listing.json",
        ]
        for path in manifests:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(payload["version"], expected, path)
            if path.name == "marketplace.json" and "plugins" in payload:
                self.assertTrue(payload["plugins"], path)
                self.assertEqual(payload["plugins"][0]["version"], expected, path)

    def test_manifest_declares_three_distinct_router_layers(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        routing = manifest["routing"]
        expected = {
            "skill_router": "scripts/skill_router.py",
            "dynamic_router": "scripts/dynamic_router.py",
            "neural_router": "scripts/neural_router.py",
            "skill_routes": "routing/skill-routes.json",
            "execution_bindings": "routing/skill-execution-bindings.json",
        }
        for key, relative in expected.items():
            self.assertEqual(routing.get(key), relative, key)
            self.assertTrue((ROOT / relative).is_file(), relative)
        self.assertEqual(len({routing[key] for key in ("skill_router", "dynamic_router", "neural_router")}), 3)

    def test_release_docs_reference_current_not_previous_release(self):
        current = self.current_version()
        previous = self.previous_minor_version(current)
        surfaces = [
            ROOT / "README.md",
            ROOT / "adapters" / "openai" / "README.md",
            ROOT / "adapters" / "claude" / "README.md",
            ROOT / ".agents" / "skills" / "marketing-council-pack" / "SKILL.md",
            ROOT / ".claude" / "skills" / "marketing-council-pack" / "SKILL.md",
        ]
        for path in surfaces:
            text = path.read_text(encoding="utf-8")
            self.assertIn(current, text, path)
            if previous:
                self.assertNotIn(previous, text, path)

    def test_readme_documents_dynamic_router_and_full_pack_execution_bindings(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("scripts/skill_router.py", text)
        self.assertIn("scripts/dynamic_router.py", text)
        self.assertIn("scripts/neural_router.py", text)
        self.assertIn("routing/skill-execution-bindings.json", text)
        self.assertIn("three routing layers", text.lower())


if __name__ == "__main__":
    unittest.main()
