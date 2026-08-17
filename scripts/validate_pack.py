#!/usr/bin/env python3
"""Validate Marketing Council structure and Agent Skills frontmatter without third-party packages."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = {}
    for line in parts[1].strip().splitlines():
        if line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate_pack(root: str | Path) -> dict:
    root = Path(root)
    errors: list[str] = []
    warnings: list[str] = []
    required_dirs = ["skills", "agents", "hooks", "workflows", "references", "neural"]
    for name in required_dirs:
        if not (root / name).is_dir():
            errors.append(f"missing required directory: {name}")

    skill_files = sorted((root / "skills").glob("*/SKILL.md")) if (root / "skills").exists() else []
    if (root / "SKILL.md").exists():
        skill_files = [root / "SKILL.md", *skill_files]
    if not skill_files:
        errors.append("no SKILL.md files found")
    for path in skill_files:
        fm = _frontmatter(path)
        name = fm.get("name", "")
        desc = fm.get("description", "")
        expected_name = root.name if path == root / "SKILL.md" else path.parent.name
        if name != expected_name:
            errors.append(f"{path}: frontmatter name must match directory")
        if not NAME_RE.fullmatch(name):
            errors.append(f"{path}: invalid skill name")
        if not desc:
            errors.append(f"{path}: missing description")
        elif len(desc) > 1024:
            errors.append(f"{path}: description exceeds 1024 characters")
        elif not desc.startswith("Use when"):
            warnings.append(f"{path}: description should start with 'Use when' for discovery")
        if len(path.read_text(encoding="utf-8").splitlines()) > 500:
            warnings.append(f"{path}: over 500 lines; split for progressive disclosure")


    graph_path = root / "neural" / "graph.json"
    if graph_path.is_file():
        try:
            graph = json.loads(graph_path.read_text(encoding="utf-8"))
            ids = {node.get("id") for node in graph.get("nodes", [])}
            if len(ids) != len(graph.get("nodes", [])):
                errors.append("neural graph has duplicate node ids")
            for edge in graph.get("edges", []):
                if edge.get("from") not in ids or edge.get("to") not in ids:
                    errors.append(f"neural graph has dangling edge: {edge}")
        except Exception as exc:
            errors.append(f"neural graph unreadable: {exc}")

    corpus = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.glob("**/*.md"))
    for phrase in ("you are philip kotler", "you are seth godin", "you are steve jobs", "pretend to be philip kotler"):
        if phrase in corpus.lower():
            errors.append(f"celebrity role-play instruction found: {phrase}")

    return {
        "valid": not errors,
        "skill_count": len(skill_files),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Validate a Marketing Council pack.")
    p.add_argument("root", nargs="?", default=Path(__file__).resolve().parents[1], type=Path)
    args = p.parse_args()
    result = validate_pack(args.root)
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
