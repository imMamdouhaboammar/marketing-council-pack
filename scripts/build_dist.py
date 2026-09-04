#!/usr/bin/env python3
"""Build a self-contained, uploadable Marketing Council Agent Skill directory."""
from __future__ import annotations
import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def reject_symlink(path: Path, source_root: Path) -> None:
    if path.is_symlink():
        try:
            rel = path.relative_to(source_root)
        except ValueError:
            rel = path
        raise ValueError(f"symlink source not allowed: {rel}")


def copy_tree_clean(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    reject_symlink(src, src)
    for path in src.rglob('*'):
        reject_symlink(path, src)
        if path.is_dir():
            continue
        if '__pycache__' in path.parts or path.suffix in {'.pyc', '.pyo'}:
            continue
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def build_dist(output: Path) -> Path:
    output = output.resolve()
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)

    source_main = ROOT / 'skills' / 'marketing-council' / 'SKILL.md'
    reject_symlink(source_main, ROOT)
    text = source_main.read_text(encoding='utf-8')
    replacements = {
        '../../agents/': 'agents/',
        '../../hooks/': 'hooks/',
        '../../scripts/': 'scripts/',
        '../../workflows/': 'workflows/',
        '../../references/': 'references/',
        '../../tools/': 'tools/',
        '../../neural/': 'neural/',
        '../../routing/': 'routing/',
        'load the matching focused skill under `../`': 'load the matching focused module under `skills/`',
        'load a focused sibling skill': 'load a focused module from `skills/`',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    (output / 'SKILL.md').write_text(text, encoding='utf-8')

    copy_tree_clean(ROOT / 'agents', output / 'agents')
    copy_tree_clean(ROOT / 'hooks', output / 'hooks')
    copy_tree_clean(ROOT / 'workflows', output / 'workflows')
    copy_tree_clean(ROOT / 'references', output / 'references')
    copy_tree_clean(ROOT / 'tools', output / 'tools')
    copy_tree_clean(ROOT / 'scripts', output / 'scripts')
    copy_tree_clean(ROOT / 'neural', output / 'neural')
    copy_tree_clean(ROOT / 'routing', output / 'routing')

    for skill_dir in (ROOT / 'skills').iterdir():
        reject_symlink(skill_dir, ROOT / 'skills')
        if not skill_dir.is_dir() or skill_dir.name == 'marketing-council':
            continue
        copy_tree_clean(skill_dir, output / 'skills' / skill_dir.name)

    for source, target in (
        (ROOT / 'LICENSE', output / 'LICENSE'),
        (ROOT / 'manifest.json', output / 'manifest.json'),
    ):
        reject_symlink(source, ROOT)
        shutil.copy2(source, target)
    return output


def main() -> None:
    p = argparse.ArgumentParser(description='Build a self-contained Marketing Council skill directory.')
    p.add_argument('--output', type=Path, default=ROOT / 'dist' / 'marketing-council')
    args = p.parse_args()
    built = build_dist(args.output)
    print(built)


if __name__ == '__main__':
    main()
