import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}
    _, fm, _ = text.split('---', 2)
    data = {}
    for line in fm.strip().splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            data[key.strip()] = value.strip().strip('"')
    return data


class PackStructureTests(unittest.TestCase):
    def test_main_skill_exists_and_has_valid_frontmatter(self):
        path = ROOT / 'skills' / 'marketing-council' / 'SKILL.md'
        self.assertTrue(path.exists())
        fm = parse_frontmatter(path)
        self.assertEqual(fm.get('name'), 'marketing-council')
        self.assertTrue(fm.get('description', '').startswith('Use when'))
        self.assertRegex(fm['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
        self.assertLessEqual(len(fm['description']), 1024)

    def test_main_skill_is_progressive_disclosure_friendly(self):
        path = ROOT / 'skills' / 'marketing-council' / 'SKILL.md'
        self.assertLessEqual(len(path.read_text(encoding='utf-8').splitlines()), 500)

    def test_all_required_agents_exist(self):
        names = {
            'council-director', 'market-architect', 'positioning-strategist',
            'audience-strategist', 'product-marketing-director', 'response-strategist',
            'awareness-strategist', 'behavior-strategist', 'brand-growth-strategist',
            'commercial-strategist', 'channel-strategist', 'marketing-skeptic',
            'brand-equity-strategist', 'creative-strategist', 'effectiveness-strategist',
            'competitive-strategy-analyst', 'lifecycle-strategist', 'measurement-strategist', 'commerce-media-strategist', 'creator-commerce-strategist', 'marketing-signal-architect', 'marketing-automation-governor', 'agentic-commerce-strategist', 'ai-discovery-strategist'
        }
        existing = {p.stem for p in (ROOT / 'agents').glob('*.md')}
        self.assertTrue(names.issubset(existing), names - existing)

    def test_all_skill_names_match_directory(self):
        for skill_file in (ROOT / 'skills').glob('*/SKILL.md'):
            fm = parse_frontmatter(skill_file)
            self.assertEqual(fm.get('name'), skill_file.parent.name, skill_file)
            self.assertRegex(fm['name'], r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

    def test_no_celebrity_roleplay_instruction(self):
        corpus = '\n'.join(p.read_text(encoding='utf-8') for p in ROOT.glob('**/*.md'))
        banned = [
            'you are philip kotler', 'you are seth godin', 'you are steve jobs',
            'pretend to be philip kotler', 'imitate steve jobs'
        ]
        lower = corpus.lower()
        for phrase in banned:
            self.assertNotIn(phrase, lower)

    def test_focused_skills_exist(self):
        required = {
            "market-diagnosis", "customer-research", "positioning-strategy",
            "offer-strategy", "pricing-strategy", "go-to-market",
            "campaign-strategy", "media-strategy", "content-strategy",
            "conversion-strategy", "retention-strategy", "marketing-experimentation",
            "competitive-intelligence", "brand-strategy", "product-marketing",
            "segmentation-strategy", "category-strategy", "behavioral-marketing",
            "marketing-measurement", "commerce-media-strategy", "creator-commerce", "incrementality-design", "marketing-signal-strategy", "autonomous-media-operations", "commerce-feed-intelligence", "agentic-commerce", "conversational-advertising", "ai-discovery-strategy"
        }
        existing = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}
        self.assertTrue(required.issubset(existing), required - existing)

    def test_required_hooks_and_workflows_exist(self):
        hooks = {
            "strategy-before-tactics", "evidence-gate", "freshness-check",
            "commercial-reality-check", "anti-generic-marketing", "pre-mortem",
            "post-strategy-red-team", "customer-language-check", "theory-fit-gate",
            "school-conflict-gate", "causal-mechanism-check", "category-maturity-check",
            "decision-stage-check", "horizon-balance-check", "closed-loop-bias-check", "creator-measurement-check", "creative-provenance-check", "incrementality-required", "automation-black-box-check", "automation-authority-check", "marketing-signal-quality", "commerce-feed-readiness", "agentic-commerce-readiness", "ai-surface-check"
        }
        workflows = {"full-strategy", "launch", "campaign", "audit", "council-debate"}
        self.assertTrue(hooks.issubset({p.stem for p in (ROOT / "hooks").glob("*.md")}))
        self.assertTrue(workflows.issubset({p.stem for p in (ROOT / "workflows").glob("*.md")}))

    def test_main_skill_links_principle_canon_and_tool_contracts(self):
        text = (ROOT / "skills" / "marketing-council" / "SKILL.md").read_text(encoding="utf-8")
        for name in ("kotler", "godin", "jobs-product-principles", "ogilvy", "schwartz", "sharp", "binet-field"):
            self.assertIn(f"../../references/canon/{name}.md", text)
        self.assertIn("../../tools/capabilities.yml", text)


if __name__ == '__main__':
    unittest.main()
