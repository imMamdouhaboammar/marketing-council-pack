import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvalSuiteTests(unittest.TestCase):
    def _files(self, kind):
        return sorted((ROOT / 'evals' / kind).glob('*.yml'))

    def test_core_and_adversarial_case_counts(self):
        self.assertGreaterEqual(len(self._files('cases')), 8)
        self.assertGreaterEqual(len(self._files('adversarial')), 5)

    def test_eval_files_have_required_contract(self):
        required = ('id:', 'title:', 'prompt:', 'expected_behaviors:', 'forbidden_behaviors:')
        ids = set()
        for path in self._files('cases') + self._files('adversarial'):
            text = path.read_text(encoding='utf-8')
            for key in required:
                self.assertIn(key, text, f'{path}: missing {key}')
            match = re.search(r'^id:\s*([a-z0-9-]+)\s*$', text, flags=re.M)
            self.assertIsNotNone(match, path)
            self.assertNotIn(match.group(1), ids, f'duplicate eval id {match.group(1)}')
            ids.add(match.group(1))

    def test_rubric_covers_decision_quality(self):
        text = (ROOT / 'evals' / 'RUBRIC.md').read_text(encoding='utf-8').lower()
        for phrase in ('diagnosis', 'evidence', 'economics', 'measurement', 'uncertainty', 'strategy from tactics'):
            self.assertIn(phrase, text)

    def test_examples_exist(self):
        expected = {'full-strategy-example', 'council-debate-example', 'starter-prompts'}
        existing = {p.stem for p in (ROOT / 'examples').glob('*.md')}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_tool_contracts_exist(self):
        self.assertTrue((ROOT / 'tools' / 'README.md').exists())
        self.assertTrue((ROOT / 'tools' / 'capabilities.yml').exists())


if __name__ == '__main__':
    unittest.main()
