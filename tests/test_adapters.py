import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.validate_pack import validate_pack


class AdapterTests(unittest.TestCase):
    def test_manifest_declares_core_components(self):
        manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['name'], 'marketing-council')
        self.assertEqual(manifest['version'], '1.5.0')
        self.assertEqual(manifest['entry_skill'], 'skills/marketing-council/SKILL.md')
        self.assertGreaterEqual(len(manifest['focused_skills']), 10)
        self.assertIn('claude', manifest['adapters'])
        self.assertIn('openai', manifest['adapters'])
        self.assertIn('copilot', manifest['adapters'])

    def test_adapter_docs_exist(self):
        for name in ('generic', 'claude', 'openai', 'copilot'):
            path = ROOT / 'adapters' / name / 'README.md'
            self.assertTrue(path.exists(), path)
            self.assertIn('Marketing Council', path.read_text(encoding='utf-8'))

    def test_build_dist_creates_self_contained_skill(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'marketing-council'
            subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_dist.py'), '--output', str(out)], check=True)
            self.assertTrue((out / 'SKILL.md').exists())
            self.assertTrue((out / 'agents' / 'marketing-skeptic.md').exists())
            self.assertTrue((out / 'hooks' / 'freshness-check.md').exists())
            self.assertTrue((out / 'skills' / 'positioning-strategy' / 'SKILL.md').exists())
            self.assertTrue((out / 'scripts' / 'unit_economics.py').exists())
            self.assertTrue((out / 'tools' / 'capabilities.yml').exists())
            self.assertTrue((out / 'neural' / 'graph.json').exists())
            main = (out / 'SKILL.md').read_text(encoding='utf-8')
            self.assertNotIn('../../agents/', main)
            self.assertNotIn('../../hooks/', main)
            self.assertIn('agents/council-director.md', main)
            result = validate_pack(out)
            self.assertTrue(result['valid'], result['errors'])
            self.assertEqual(result['skill_count'], 29)

    def test_build_dist_rejects_symlink_sources(self):
        path = ROOT / "scripts" / "build_dist.py"
        spec = importlib.util.spec_from_file_location("build_dist_under_test", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            outside = root / "outside.txt"
            outside.write_text("must not be packaged", encoding="utf-8")
            source = root / "source"
            source.mkdir()
            (source / "leak.txt").symlink_to(outside)
            with self.assertRaises(ValueError):
                module.copy_tree_clean(source, root / "dest")

    def test_install_helpers_are_present(self):
        self.assertTrue((ROOT / 'install.sh').exists())
        self.assertTrue((ROOT / 'install.ps1').exists())


if __name__ == '__main__':
    unittest.main()
