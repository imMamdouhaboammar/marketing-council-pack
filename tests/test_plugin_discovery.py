import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "1.4.0"


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def skill_definitions():
    return sorted((ROOT / "skills").glob("*/SKILL.md"))


def openai_metadata(definition: Path) -> tuple[str, Path]:
    metadata = definition.parent / "agents" / "openai.yaml"
    return metadata.read_text(encoding="utf-8") if metadata.exists() else "", metadata


class PluginDiscoveryTests(unittest.TestCase):
    def test_release_version_is_consistent_across_public_manifests(self):
        root_manifest = read_json(ROOT / "manifest.json")
        openai_manifest = read_json(ROOT / ".codex-plugin" / "plugin.json")
        claude_manifest = read_json(ROOT / ".claude-plugin" / "plugin.json")
        claude_marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
        listing = read_json(ROOT / "submission" / "listing.json")
        self.assertEqual(root_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(openai_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(claude_manifest["version"], EXPECTED_VERSION)
        self.assertEqual(claude_marketplace["version"], EXPECTED_VERSION)
        self.assertEqual(claude_marketplace["plugins"][0]["version"], EXPECTED_VERSION)
        self.assertEqual(listing["version"], EXPECTED_VERSION)

    def test_dynamic_router_exists_and_covers_every_focused_skill(self):
        router_path = ROOT / "routing" / "skill-routes.json"
        self.assertTrue(router_path.exists(), router_path)
        router = read_json(router_path)
        self.assertEqual(router["version"], 1)
        self.assertEqual(router["fallback_skill"], "marketing-council")
        skill_names = {path.parent.name for path in skill_definitions()}
        focused = skill_names - {"marketing-council"}
        routed = {route["skill"] for route in router["routes"]}
        self.assertEqual(routed, focused)
        self.assertEqual(len(router["routes"]), len(focused))
        for route in router["routes"]:
            self.assertTrue(route.get("intents"), route)
            self.assertIsInstance(route.get("priority"), int, route)
            self.assertTrue(route.get("examples"), route)
            self.assertTrue(route.get("negative_examples"), route)

    def test_executable_router_selects_narrow_skills_and_falls_back_for_cross_functional(self):
        script = ROOT / "scripts" / "skill_router.py"
        self.assertTrue(script.exists(), script)
        cases = {
            "Help me set a pricing architecture and discount guardrails": "pricing-strategy",
            "Design a geo holdout to estimate incremental ROAS": "incrementality-design",
            "Improve our creator affiliate program and creator measurement": "creator-commerce",
        }
        for prompt, expected in cases.items():
            result = subprocess.run(
                [sys.executable, str(script), "--text", prompt, "--json"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["selected_skill"], expected, payload)
            self.assertFalse(payload["fallback"], payload)

        result = subprocess.run(
            [sys.executable, str(script), "--text", "Build the complete marketing strategy across positioning, pricing, media, campaign, retention, and measurement", "--json"],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["selected_skill"], "marketing-council", payload)
        self.assertTrue(payload["fallback"], payload)

    def test_main_skill_declares_dynamic_router_and_safe_fallback(self):
        text = (ROOT / "skills" / "marketing-council" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("../../routing/skill-routes.json", text)
        self.assertRegex(text.lower(), r"dynamic\s+router")
        self.assertIn("fallback", text.lower())
        self.assertIn("single dominant function", text.lower())
        self.assertIn("cross-functional", text.lower())

    def test_all_skills_have_openai_metadata_files(self):
        skills = skill_definitions()
        self.assertEqual(len(skills), 29)
        for definition in skills:
            _, metadata = openai_metadata(definition)
            self.assertTrue(metadata.exists(), metadata)

    def test_all_skills_allow_implicit_invocation(self):
        for definition in skill_definitions():
            text, metadata = openai_metadata(definition)
            self.assertIn("allow_implicit_invocation: true", text, metadata)

    def test_all_skills_have_explicit_default_prompts(self):
        for definition in skill_definitions():
            slug = definition.parent.name
            text, metadata = openai_metadata(definition)
            self.assertIn(f"${slug}", text, metadata)
            self.assertRegex(text, r"(?m)^\s*default_prompt:\s*\"[^\"\n]+\"\s*$", metadata)

    def test_all_skills_have_renderable_interface_labels(self):
        for definition in skill_definitions():
            text, metadata = openai_metadata(definition)
            self.assertRegex(text, r"(?m)^\s*display_name:\s*\"[^\"\n]+\"\s*$", metadata)
            self.assertRegex(text, r"(?m)^\s*short_description:\s*\"[^\"\n]{25,64}\"\s*$", metadata)

    def test_all_skills_have_explicit_openai_discovery_metadata(self):
        self.test_all_skills_have_openai_metadata_files()
        self.test_all_skills_allow_implicit_invocation()
        self.test_all_skills_have_explicit_default_prompts()
        self.test_all_skills_have_renderable_interface_labels()

    def test_skill_descriptions_are_discriminative_enough_for_implicit_routing(self):
        descriptions = {}
        for definition in skill_definitions():
            text = definition.read_text(encoding="utf-8")
            match = re.search(r"(?m)^description:\s*(.+)$", text)
            self.assertIsNotNone(match, definition)
            description = match.group(1).strip().strip('"')
            self.assertTrue(description.startswith("Use when"), definition)
            self.assertGreaterEqual(len(description), 80, definition)
            descriptions[definition.parent.name] = description.casefold()
        self.assertEqual(len(set(descriptions.values())), 29)

    def test_submission_builder_outputs_29_self_contained_skill_bundles(self):
        builder = ROOT / "scripts" / "build_openai_submission_pack.py"
        self.assertTrue(builder.exists(), builder)
        with tempfile.TemporaryDirectory() as td:
            result = subprocess.run(
                [sys.executable, str(builder), "--output-root", td, "--json"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["version"], EXPECTED_VERSION)
            self.assertEqual(payload["skill_bundle_count"], 29)

            inventory = read_json(Path(td) / "submission-inventory.json")
            self.assertEqual(len(inventory["skills"]), 29)
            self.assertEqual({item["name"] for item in inventory["skills"]}, {
                path.parent.name for path in skill_definitions()
            })

            archives = sorted((Path(td) / "skills").glob("*.zip"))
            self.assertEqual(len(archives), 29)
            for archive in archives:
                with zipfile.ZipFile(archive) as zf:
                    names = set(zf.namelist())
                    skill_md = [name for name in names if name.endswith("/SKILL.md")]
                    self.assertEqual(len(skill_md), 1, archive)
                    text = zf.read(skill_md[0]).decode("utf-8")
                    self.assertNotIn("../../", text, archive)
                    self.assertIn("/agents/openai.yaml", "\n".join(sorted(names)), archive)

    def test_public_surfaces_report_29_total_and_28_focused_skills(self):
        manifest = read_json(ROOT / "manifest.json")
        openai = read_json(ROOT / ".codex-plugin" / "plugin.json")
        claude = read_json(ROOT / ".claude-plugin" / "plugin.json")
        listing = read_json(ROOT / "submission" / "listing.json")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual(len(skill_definitions()), 29)
        self.assertEqual(len(manifest["focused_skills"]), 28)
        self.assertNotIn("29 focused skills", manifest["description"].lower())
        self.assertNotIn("29 focused skills", openai["description"].lower())
        self.assertNotIn("29 focused skills", claude["description"].lower())
        self.assertNotIn("29 focused skills", listing["description"].lower())
        self.assertNotIn("29 focused skills", readme.lower())
        self.assertIn("29 Agent Skills", readme)
        self.assertIn("28 focused", readme)
        self.assertIn("version-1.4.0", readme)
        self.assertIn("Agent%20Skills-29", readme)
        self.assertIn("Specialist%20Agents-24", readme)

    def test_plugin_ci_runs_for_main_pushes_and_pull_requests(self):
        workflow = (ROOT / ".github" / "workflows" / "plugin-ci.yml").read_text(encoding="utf-8")
        self.assertRegex(workflow, r"(?ms)push:\s*branches:\s*-\s+main")
        self.assertRegex(workflow, r"(?ms)pull_request:\s*branches:\s*-\s+main")

    def test_release_notes_include_resubmission_requirement_for_snapshot_skills(self):
        path = ROOT / "docs" / "OPENAI_RELEASE.md"
        self.assertTrue(path.exists(), path)
        text = path.read_text(encoding="utf-8").lower()
        self.assertIn("snapshot", text)
        self.assertIn("resubmit", text)
        self.assertIn("29", text)
        self.assertIn("plugin submission", text)
        self.assertIn("standalone", text)


if __name__ == "__main__":
    unittest.main()
