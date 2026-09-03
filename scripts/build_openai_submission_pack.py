#!/usr/bin/env python3
"""Build a reviewer-ready OpenAI submission pack with standalone skill bundles.

OpenAI skills are versioned bundles of files. The repository uses shared agents,
hooks, references, routers, and deterministic scripts, so this builder copies
those dependencies inside each skill archive and rewrites package-relative
references. The result does not rely on files outside the submitted skill.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from build_host_packages import build_openai, version

ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (2026, 9, 3, 0, 0, 0)
SHARED_DIRS = (
    "agents",
    "hooks",
    "references",
    "neural",
    "scripts",
    "tools",
    "workflows",
    "routing",
)
SKIP_PARTS = {"__pycache__", ".pytest_cache", ".DS_Store", "dist", ".git"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def reject_symlink(path: Path, source_root: Path) -> None:
    if path.is_symlink():
        try:
            rel = path.relative_to(source_root)
        except ValueError:
            rel = path
        raise ValueError(f"symlink source not allowed: {rel}")


def copy_clean(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    reject_symlink(src, src)
    for path in sorted(src.rglob("*")):
        reject_symlink(path, src)
        if path.is_dir():
            continue
        rel = path.relative_to(src)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def rewrite_skill_paths(text: str) -> str:
    """Rewrite a standalone skill root to use bundle-local shared resources."""
    rewritten = text
    for directory in SHARED_DIRS:
        rewritten = rewritten.replace(f"../../{directory}/", f"shared/{directory}/")
    rewritten = rewritten.replace(
        "load the matching focused skill under `../`",
        "load the matching focused module under `skills/`",
    )
    rewritten = rewritten.replace(
        "load a focused sibling skill",
        "load a focused module from `skills/`",
    )
    return rewritten


def rewrite_nested_module_paths(text: str) -> str:
    """Rewrite a focused module nested at skills/<slug>/ inside the council bundle."""
    rewritten = text
    for directory in SHARED_DIRS:
        rewritten = rewritten.replace(
            f"../../{directory}/",
            f"../../shared/{directory}/",
        )
    return rewritten


def copy_focused_module(src: Path, dst: Path) -> None:
    """Copy one focused skill into the council bundle with valid nested paths."""
    dst.mkdir(parents=True, exist_ok=True)
    reject_symlink(src, src)
    for path in sorted(src.rglob("*")):
        reject_symlink(path, src)
        if path.is_dir():
            continue
        rel = path.relative_to(src)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if rel.as_posix() == "SKILL.md":
            text = rewrite_nested_module_paths(path.read_text(encoding="utf-8"))
            target.write_text(text, encoding="utf-8")
        else:
            shutil.copy2(path, target)


def deterministic_zip(source: Path, archive: Path, prefix: str) -> Path:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        archive.unlink()
    reject_symlink(source, source)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(source.rglob("*")):
            reject_symlink(path, source)
            if not path.is_file():
                continue
            rel = path.relative_to(source).as_posix()
            info = zipfile.ZipInfo(f"{prefix}/{rel}", FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return archive


def build_skill_bundle(skill_dir: Path, output_dir: Path, ver: str) -> Path:
    reject_symlink(skill_dir, skill_dir)
    slug = skill_dir.name
    with tempfile.TemporaryDirectory() as td:
        bundle = Path(td) / slug
        bundle.mkdir(parents=True)

        source_skill = skill_dir / "SKILL.md"
        reject_symlink(source_skill, skill_dir)
        text = rewrite_skill_paths(source_skill.read_text(encoding="utf-8"))
        if "../../" in text:
            raise ValueError(f"unresolved external path remains in {source_skill}")
        (bundle / "SKILL.md").write_text(text, encoding="utf-8")

        for child in sorted(skill_dir.iterdir()):
            reject_symlink(child, skill_dir)
            if child.name == "SKILL.md":
                continue
            target = bundle / child.name
            if child.is_dir():
                copy_clean(child, target)
            elif child.is_file():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(child, target)

        shared = bundle / "shared"
        for directory in SHARED_DIRS:
            copy_clean(ROOT / directory, shared / directory)

        if slug == "marketing-council":
            for focused_dir in sorted((ROOT / "skills").iterdir()):
                if not focused_dir.is_dir() or focused_dir.name == slug:
                    continue
                copy_focused_module(
                    focused_dir,
                    bundle / "skills" / focused_dir.name,
                )

        metadata = bundle / "agents" / "openai.yaml"
        if not metadata.is_file():
            raise ValueError(f"missing agents/openai.yaml for {slug}")

        return deterministic_zip(
            bundle,
            output_dir / f"{slug}-v{ver}.zip",
            prefix=slug,
        )


def build_submission_pack(output_root: Path) -> dict:
    ver = version()
    output_root.mkdir(parents=True, exist_ok=True)
    skill_output = output_root / "skills"
    plugin_output = output_root / "plugin"

    for directory in (skill_output, plugin_output):
        if directory.exists():
            shutil.rmtree(directory)
        directory.mkdir(parents=True, exist_ok=True)

    plugin_archive = build_openai(plugin_output, ver)
    skills = []
    for definition in sorted((ROOT / "skills").glob("*/SKILL.md")):
        archive = build_skill_bundle(definition.parent, skill_output, ver)
        skills.append({
            "name": definition.parent.name,
            "archive": archive.relative_to(output_root).as_posix(),
            "sha256": sha256(archive),
            "bytes": archive.stat().st_size,
            "standalone": True,
        })

    inventory = {
        "plugin": "marketing-council",
        "version": ver,
        "architecture": "skills-only",
        "plugin_archive": {
            "path": plugin_archive.relative_to(output_root).as_posix(),
            "sha256": sha256(plugin_archive),
            "bytes": plugin_archive.stat().st_size,
        },
        "skill_count": len(skills),
        "skills": skills,
        "submission_note": (
            "OpenAI public releases use submitted skill snapshots. Resubmit all "
            "29 standalone skill bundles whenever public skill content changes."
        ),
    }
    inventory_path = output_root / "submission-inventory.json"
    inventory_path.write_text(json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "version": ver,
        "plugin_archive": str(plugin_archive),
        "skill_bundle_count": len(skills),
        "inventory": str(inventory_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the OpenAI submission pack for Marketing Council.")
    parser.add_argument("--output-root", type=Path, default=ROOT / "dist" / "openai-submission")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = build_submission_pack(args.output_root.resolve())
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"OpenAI submission pack: {result['skill_bundle_count']} skills; version {result['version']}")


if __name__ == "__main__":
    main()
