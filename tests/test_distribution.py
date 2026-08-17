import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def simple_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    _, block, _ = text.split("---", 2)
    out = {}
    for line in block.splitlines():
        if not line.strip() or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        out[key.strip()] = value.strip().strip('"')
    return out


class DistributionTests(unittest.TestCase):
    def test_release_version_is_1_3_0(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "1.3.0")
        for skill in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertIn('version: "1.3.0"', skill.read_text(encoding="utf-8"), skill)

    def test_openai_plugin_manifest(self):
        path = ROOT / ".codex-plugin" / "plugin.json"
        self.assertTrue(path.exists(), path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["name"], "marketing-council")
        self.assertEqual(data["version"], "1.3.0")
        self.assertEqual(data["skills"], "./skills/")
        self.assertEqual(data["repository"], "https://github.com/imMamdouhaboammar/marketing-council-pack")
        self.assertLessEqual(len(data["interface"]["displayName"]), 30)
        self.assertLessEqual(len(data["interface"]["shortDescription"]), 30)
        self.assertLessEqual(len(data["interface"]["capabilities"]), 20)
        self.assertLessEqual(len(data["interface"]["defaultPrompt"]), 3)
        for prompt in data["interface"]["defaultPrompt"]:
            self.assertLessEqual(len(prompt), 128)
            self.assertNotIn("@", prompt)
        for key in ("logo", "composerIcon"):
            asset = ROOT / data["interface"][key].removeprefix("./")
            self.assertTrue(asset.exists(), asset)

    def test_openai_repo_marketplace(self):
        path = ROOT / ".agents" / "plugins" / "marketplace.json"
        self.assertTrue(path.exists(), path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["plugins"][0]["name"], "marketing-council")
        self.assertEqual(data["plugins"][0]["source"]["source"], "url")
        self.assertIn("marketing-council-pack", data["plugins"][0]["source"]["url"])

    def test_every_skill_has_openai_metadata(self):
        skills = sorted((ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skills), 29)
        for skill in skills:
            metadata = skill.parent / "agents" / "openai.yaml"
            self.assertTrue(metadata.exists(), metadata)
            text = metadata.read_text(encoding="utf-8")
            self.assertIn("interface:", text)
            self.assertIn("display_name:", text)
            self.assertIn("short_description:", text)
            self.assertIn("default_prompt:", text)

    def test_claude_plugin_and_marketplace(self):
        plugin = ROOT / ".claude-plugin" / "plugin.json"
        market = ROOT / ".claude-plugin" / "marketplace.json"
        self.assertTrue(plugin.exists(), plugin)
        self.assertTrue(market.exists(), market)
        pdata = json.loads(plugin.read_text(encoding="utf-8"))
        mdata = json.loads(market.read_text(encoding="utf-8"))
        self.assertEqual(pdata["name"], "marketing-council")
        self.assertEqual(pdata["version"], "1.3.0")
        self.assertEqual(pdata["skills"], "./skills/")
        self.assertEqual(pdata["agents"], "./agents/")
        self.assertEqual(mdata["name"], "marketing-council")
        self.assertEqual(mdata["plugins"][0]["name"], "marketing-council")
        self.assertEqual(mdata["plugins"][0]["source"]["source"], "github")
        self.assertEqual(mdata["plugins"][0]["source"]["repo"], "imMamdouhaboammar/marketing-council-pack")

    def test_all_role_docs_are_valid_claude_agents(self):
        agents = sorted((ROOT / "agents").glob("*.md"))
        self.assertEqual(len(agents), 24)
        for path in agents:
            fm = simple_frontmatter(path)
            self.assertEqual(fm.get("name"), path.stem, path)
            self.assertTrue(fm.get("description", "").startswith("Use when"), path)

    def test_readme_contains_verified_install_surfaces(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        required = [
            "npx skills add imMamdouhaboammar/marketing-council-pack --all -y",
            "-a codex",
            "-a claude-code",
            "codex plugin marketplace add imMamdouhaboammar/marketing-council-pack",
            "/plugin marketplace add imMamdouhaboammar/marketing-council-pack",
            "/plugin install marketing-council@marketing-council",
        ]
        for item in required:
            self.assertIn(item, text)

    def test_host_package_builder_outputs_expected_archives(self):
        script = ROOT / "scripts" / "build_host_packages.py"
        self.assertTrue(script.exists(), script)
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([sys.executable, str(script), "--output-root", td], check=True)
            out = Path(td)
            expected = {
                "marketing-council-openai-plugin-v1.3.0.zip",
                "marketing-council-claude-marketplace-v1.3.0.zip",
                "marketing-council-skill-v1.3.0.zip",
            }
            self.assertTrue(expected.issubset({p.name for p in out.glob("*.zip")}))

    def test_host_packages_are_complete_and_deterministic(self):
        import hashlib
        import zipfile

        script = ROOT / "scripts" / "build_host_packages.py"
        self.assertTrue(script.exists(), script)
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            subprocess.run([sys.executable, str(script), "--output-root", a], check=True)
            subprocess.run([sys.executable, str(script), "--output-root", b], check=True)

            names = [
                "marketing-council-openai-plugin-v1.3.0.zip",
                "marketing-council-claude-marketplace-v1.3.0.zip",
                "marketing-council-skill-v1.3.0.zip",
            ]
            for name in names:
                one = Path(a) / name
                two = Path(b) / name
                self.assertEqual(hashlib.sha256(one.read_bytes()).hexdigest(), hashlib.sha256(two.read_bytes()).hexdigest(), name)

            with zipfile.ZipFile(Path(a) / names[0]) as zf:
                entries = set(zf.namelist())
                self.assertIn(".codex-plugin/plugin.json", entries)
                self.assertIn("agents/marketing-skeptic.md", entries)
                self.assertEqual(sum(1 for e in entries if e.startswith("skills/") and e.endswith("/SKILL.md")), 29)

            with zipfile.ZipFile(Path(a) / names[1]) as zf:
                entries = set(zf.namelist())
                self.assertIn(".claude-plugin/marketplace.json", entries)
                prefix = "plugins/marketing-council/"
                self.assertIn(prefix + ".claude-plugin/plugin.json", entries)
                self.assertEqual(sum(1 for e in entries if e.startswith(prefix + "skills/") and e.endswith("/SKILL.md")), 29)
                self.assertEqual(sum(1 for e in entries if e.startswith(prefix + "agents/") and e.endswith(".md")), 24)

            with zipfile.ZipFile(Path(a) / names[2]) as zf:
                entries = set(zf.namelist())
                self.assertIn("marketing-council/SKILL.md", entries)
                self.assertIn("marketing-council/agents/marketing-skeptic.md", entries)

    def test_distribution_validator_exists_and_accepts_source(self):
        script = ROOT / "scripts" / "validate_distribution.py"
        self.assertTrue(script.exists(), script)
        result = subprocess.run([sys.executable, str(script), str(ROOT), "--json"], text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["valid"], payload)
        self.assertEqual(payload["skill_count"], 29)
        self.assertEqual(payload["agent_count"], 24)

    def test_openai_public_validator_accepts_built_plugin(self):
        import zipfile

        builder = ROOT / "scripts" / "build_host_packages.py"
        validator = ROOT / "scripts" / "validate_openai_plugin.py"
        self.assertTrue(validator.exists(), validator)
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([sys.executable, str(builder), "--output-root", td], check=True, stdout=subprocess.DEVNULL)
            archive = Path(td) / "marketing-council-openai-plugin-v1.3.0.zip"
            extracted = Path(td) / "plugin"
            with zipfile.ZipFile(archive) as zf:
                zf.extractall(extracted)
            result = subprocess.run([sys.executable, str(validator), str(extracted), "--json"], text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"], payload)
            self.assertEqual(payload["architecture"], "skills-only")
            self.assertEqual(len(payload["skills"]), 29)


if __name__ == "__main__":
    unittest.main()
