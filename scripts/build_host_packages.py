#!/usr/bin/env python3
"""Build deterministic Marketing Council release archives for supported hosts."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from build_dist import build_dist

ROOT = Path(__file__).resolve().parents[1]
FIXED_ZIP_TIME = (2026, 8, 17, 0, 0, 0)
RUNTIME_DIRS = ("skills", "agents", "hooks", "references", "neural", "scripts", "tools", "workflows", "assets")
ROOT_RUNTIME_FILES = ("manifest.json", "LICENSE", "README.md", "SECURITY.md")
SOURCE_EXCLUDES = {".git", "dist", "__pycache__", ".pytest_cache", ".DS_Store"}


def version() -> str:
    return json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))["version"]


def copy_tree_clean(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    for path in sorted(src.rglob("*")):
        if path.is_dir():
            continue
        if any(part in SOURCE_EXCLUDES for part in path.parts):
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        rel = path.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def copy_runtime(dst: Path, *, plugin_manifest: str) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    manifest_src = ROOT / plugin_manifest
    manifest_dst = dst / plugin_manifest
    manifest_dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_src, manifest_dst)
    for name in RUNTIME_DIRS:
        copy_tree_clean(ROOT / name, dst / name)
    for name in ROOT_RUNTIME_FILES:
        src = ROOT / name
        if src.exists():
            shutil.copy2(src, dst / name)


def deterministic_zip(source: Path, archive: Path, *, prefix: str = "") -> Path:
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in source.rglob("*") if p.is_file()):
            rel = path.relative_to(source).as_posix()
            arcname = f"{prefix.rstrip('/')}/{rel}" if prefix else rel
            info = zipfile.ZipInfo(arcname, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.create_system = 3
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return archive


def build_openai(output_root: Path, ver: str) -> Path:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td) / "plugin"
        copy_runtime(root, plugin_manifest=".codex-plugin/plugin.json")
        return deterministic_zip(root, output_root / f"marketing-council-openai-plugin-v{ver}.zip")


def build_claude(output_root: Path, ver: str) -> Path:
    with tempfile.TemporaryDirectory() as td:
        market = Path(td) / "marketplace"
        plugin = market / "plugins" / "marketing-council"
        copy_runtime(plugin, plugin_manifest=".claude-plugin/plugin.json")

        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        marketplace["plugins"][0]["source"] = "./plugins/marketing-council"
        market_meta = market / ".claude-plugin" / "marketplace.json"
        market_meta.parent.mkdir(parents=True, exist_ok=True)
        market_meta.write_text(json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        shutil.copy2(ROOT / "README.md", market / "README.md")
        shutil.copy2(ROOT / "LICENSE", market / "LICENSE")
        return deterministic_zip(market, output_root / f"marketing-council-claude-marketplace-v{ver}.zip")


def build_skill(output_root: Path, ver: str) -> Path:
    with tempfile.TemporaryDirectory() as td:
        skill = Path(td) / "marketing-council"
        build_dist(skill)
        return deterministic_zip(skill, output_root / f"marketing-council-skill-v{ver}.zip", prefix="marketing-council")


def build_source(output_root: Path, ver: str) -> Path:
    with tempfile.TemporaryDirectory() as td:
        source = Path(td) / "marketing-council-pack"
        source.mkdir(parents=True)
        for path in sorted(ROOT.rglob("*")):
            if path.is_dir():
                continue
            rel = path.relative_to(ROOT)
            if any(part in SOURCE_EXCLUDES for part in rel.parts):
                continue
            if path.suffix in {".pyc", ".pyo"}:
                continue
            target = source / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        return deterministic_zip(source, output_root / f"marketing-council-pack-v{ver}.zip", prefix="marketing-council-pack")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_all(output_root: Path) -> list[Path]:
    ver = version()
    output_root.mkdir(parents=True, exist_ok=True)
    archives = [
        build_openai(output_root, ver),
        build_claude(output_root, ver),
        build_skill(output_root, ver),
        build_source(output_root, ver),
    ]
    sums = output_root / f"marketing-council-v{ver}-SHA256SUMS.txt"
    sums.write_text("".join(f"{sha256(path)}  {path.name}\n" for path in archives), encoding="utf-8")
    return archives


def main() -> None:
    parser = argparse.ArgumentParser(description="Build deterministic Marketing Council host packages.")
    parser.add_argument("--output-root", type=Path, default=ROOT / "dist" / "release")
    args = parser.parse_args()
    archives = build_all(args.output_root.resolve())
    print(json.dumps({"version": version(), "archives": [str(p) for p in archives]}, indent=2))


if __name__ == "__main__":
    main()
