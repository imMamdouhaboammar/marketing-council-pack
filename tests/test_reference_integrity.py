import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / 'references' / 'canon'


class ReferenceIntegrityTests(unittest.TestCase):
    def test_canon_has_expected_schools(self):
        expected = {
            'kotler', 'godin', 'jobs-product-principles', 'ogilvy', 'hopkins',
            'schwartz', 'ries-trout', 'cialdini', 'sharp', 'binet-field', 'jtbd'
        }
        existing = {p.stem for p in CANON.glob('*.md')}
        self.assertTrue(expected.issubset(existing), expected - existing)

    def test_each_canon_card_has_decision_structure(self):
        required = ['## Principle', '## Use when', '## Do not over-apply',
                    '## Decision questions', '## Counterweight', '## Sources']
        for path in CANON.glob('*.md'):
            text = path.read_text(encoding='utf-8')
            for heading in required:
                self.assertIn(heading, text, f'{path}: missing {heading}')

    def test_sources_registry_has_all_source_ids_used_by_canon(self):
        registry = (ROOT / 'references' / 'sources.yml').read_text(encoding='utf-8')
        registered = set(re.findall(r'^  ([a-z0-9-]+):$', registry, flags=re.M))
        for path in CANON.glob('*.md'):
            used = set(re.findall(r'`source:([a-z0-9-]+)`', path.read_text(encoding='utf-8')))
            self.assertTrue(used, f'{path}: no source ids')
            self.assertTrue(used.issubset(registered), f'{path}: unknown ids {used - registered}')


    def test_all_reference_cards_use_registered_sources(self):
        registry = (ROOT / "references" / "sources.yml").read_text(encoding="utf-8")
        registered = set(re.findall(r"^  ([a-z0-9-]+):$", registry, flags=re.M))
        for folder in ("canon", "figures", "theories", "2026"):
            for path in (ROOT / "references" / folder).glob("*.md"):
                used = set(re.findall(r"`source:([a-z0-9-]+)`", path.read_text(encoding="utf-8")))
                self.assertTrue(used, f"{path}: no source ids")
                self.assertTrue(used.issubset(registered), f"{path}: unknown ids {used - registered}")


    def test_figure_counterweights_reference_known_figures(self):
        figures = {p.stem for p in (ROOT / "references" / "figures").glob("*.md")}
        for path in (ROOT / "references" / "figures").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            refs = set(re.findall(r"Compare with `([a-z0-9-]+)`", text))
            self.assertTrue(refs, f"{path}: missing counterweight figure")
            self.assertTrue(refs.issubset(figures), f"{path}: unknown counterweights {refs - figures}")

    def test_decision_rules_and_frameworks_exist(self):
        rules = {p.stem for p in (ROOT / 'references' / 'decision-rules').glob('*.md')}
        frameworks = {p.stem for p in (ROOT / 'references' / 'frameworks').glob('*.md')}
        self.assertTrue({'claim-status', 'channel-choice', 'strategy-vs-tactics', 'confidence'}.issubset(rules))
        self.assertTrue({'strategy-contract', 'tactic-contract', 'research-brief', 'measurement-tree'}.issubset(frameworks))


if __name__ == '__main__':
    unittest.main()
