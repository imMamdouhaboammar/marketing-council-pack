import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.4.0"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_openai_yaml(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class PluginDiscoveryTests(unittest.TestCase):
    def test_release_version_is_consistent_across_public_manifests(self):
        root_manifest = read_json(ROOT / "manifest.json")
        openai_manifest = read_json(ROOT / ".codex-plugin" / "plugin.json")
        claude_manifest = read_json(ROOT / ".claude-plugin" / "plugin.json")
        claude_marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")

        self.assertEqual(root_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(openai_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(claude_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(claude_marketplace["version"], EXPECTED_VERSION)
        self.assertEqual(claude_marketplace["plugins"][0]["version"], EXPECTED_VERSION)

    def test_dynamic_router_exists_and_covers_every_focused_skill(self):
        router_path = ROOT / "routing" / "skill-routes.json"
        self.assertTrue(router_path.exists(), router_path)
        router = read_json(router_path)
        self.assertEqual(router["version"], 1)
        self.assertEqual(router["fallback_skill"], "marketing-council")

        skill_names = {
            path.parent.name
            for path in (ROOT / "skills").glob("*/SKILL.md")
        }
        focused = skill_names - {"marketing-council"}
        routed = {route["skill"] for route in router["routes"]}

        self.assertEqual(routed, focused)
        self.assertEqual(len(router["routes"]), len(focused))

        for route in router["routes"]:
            self.assertTrue(route.get("intents"), route)
            self.assertIsInstance(route.get("priority"), int, route)
            self.assertTrue(route.get("examples"), route)
            self.assertTrue(route.get("negative_examples"), route)

    def test_main_skill_declares_dynamic_router_and_safe_fallback(self):
        text = (ROOT / "skills" / "marketing-council" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../../routing/skill-routes.json", text)
        self.assertRegex(text.lower(), r"dynamic\s+router")
        self.assertIn("fallback", text.lower())
        self.assertIn("single dominant function", text.lower())
        self.assertIn("cross-functional", text.lower())

    def test_all_skills_have_explicit_openai_discovery_metadata(self):
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 29)

        for definition in skills:
            slug = definition.parent.name
            metadata = definition.parent / "agents" / "openai.yaml"
            self.assertTrue(metadata.exists(), metadata)
            text = read_openai_yaml(metadata)
            self.assertIn("allow_implicit_invocation: true", text, metadata)
            self.assertIn(f"${slug}", text, metadata)
            self.assertRegex(text, r"(?m)^\s*display_name:\s*\"[^\"]+\"\s*$")
            self.assertRegex(text, r"(?m)^\s*short_description:\s*\"[^\"]{25,64}\"\s*$")
            self.assertRegex(text, r"(?m)^\s*default_prompt:\s*\"[^\"]+\"\s*$")

    def test_skill_descriptions_are_discriminative_enough_for_implicit_routing(self):
        descriptions = {}
        for definition in sorted((ROOT / "skills").glob("*/SKILL.md")):
            text = definition.read_text(encoding="utf-8")
            match = re.search(r"(?m)^description:\s*(.+)$", text)
            self.assertIsNotNone(match, definition)
            description = match.group(1).strip().strip('"')
            self.assertTrue(description.startswith("Use when"), definition)
            self.assertGreaterEqual(len(description), 80, definition)
            descriptions[definition.parent.name] = description.casefold()

        self.assertEqual(len(set(descriptions.values())), 29)

    def test_release_notes_include_resubmission_requirement_for_snapshot_skills(self):
        path = ROOT / "docs" / "OPENAI_RELEASE.md"
        self.assertTrue(path.exists(), path)
        text = path.read_text(encoding="utf-8").lower()
        self.assertIn("snapshot", text)
        self.assertIn("resubmit", text)
        self.assertIn("29", text)
        self.assertIn("plugin submission", text)


if __name__ == "__main__":
    unittest.main()
