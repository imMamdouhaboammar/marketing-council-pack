#!/usr/bin/env python3
"""Public preflight for the Marketing Council ChatGPT/Codex plugin package.

This validator mirrors the release-critical checks used by the Plugin Autopilot
workflow while remaining dependency-free and repository-owned.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

MAX_ENTRIES = 5000
MAX_TOTAL = 512 * 1024 * 1024
MAX_MEMBER = 100 * 1024 * 1024
MAX_IMAGE = 5 * 1024 * 1024
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
PLUGIN_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")
CATEGORIES = {
    "Productivity", "Creativity", "Developer Tools", "Business & Operations",
    "Data & Analytics", "Communication", "Education & Research", "Security",
    "Finance", "Healthcare", "Travel", "Entertainment", "Other",
}
SECRET_BASENAME = re.compile(
    r"^(?:\.env(?:\..*)?|auth\.json|credentials?(?:\..*)?|secrets?(?:\..*)?|\.npmrc|\.pypirc)$",
    re.I,
)
TEXT_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".xml", ".py", ".sh", ".svg"}


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def https_url(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password


def luminance(color: str) -> float:
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(a: str, b: str) -> float:
    high, low = sorted((luminance(a), luminance(b)), reverse=True)
    return (high + 0.05) / (low + 0.05)


def skill_metadata(path: Path) -> tuple[str | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, None
    end = text.find("\n---", 4)
    if end < 0:
        return None, None
    block = text[4:end]
    name = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", block)
    desc = re.search(r"(?m)^description:\s*(.+)$", block)
    return (name.group(1).strip() if name else None, desc.group(1).strip().strip("\"'") if desc else None)


def validate_svg(path: Path, field: str, errors: list[str]) -> None:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        add(errors, root.tag.split("}")[-1].lower() == "svg", f"{field} root must be svg")
        view_box = root.attrib.get("viewBox") or root.attrib.get("viewbox")
        if view_box:
            values = [float(v) for v in re.split(r"[\s,]+", view_box.strip()) if v]
            add(errors, len(values) == 4 and values[2] == values[3] and values[2] >= 48, f"{field} must be square and at least 48x48")
        else:
            width = float(root.attrib.get("width", "0"))
            height = float(root.attrib.get("height", "0"))
            add(errors, width == height and width >= 48, f"{field} must be square and at least 48x48")
    except Exception as exc:
        errors.append(f"{field} SVG unreadable: {exc}")


def validate_plugin(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not root.is_dir():
        return {"ok": False, "architecture": "unknown", "skills": [], "errors": [f"plugin root is not a directory: {root}"], "warnings": []}

    manifest_path = root / ".codex-plugin" / "plugin.json"
    add(errors, manifest_path.is_file(), "missing .codex-plugin/plugin.json")
    if not manifest_path.is_file():
        return {"ok": False, "architecture": "unknown", "skills": [], "errors": errors, "warnings": warnings}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "architecture": "unknown", "skills": [], "errors": [f"manifest unreadable: {exc}"], "warnings": warnings}

    name = manifest.get("name")
    version = manifest.get("version")
    description = manifest.get("description")
    author = manifest.get("author")
    add(errors, isinstance(name, str) and bool(PLUGIN_NAME.fullmatch(name)), "invalid plugin name")
    add(errors, isinstance(version, str) and len(version) <= 64 and bool(SEMVER.fullmatch(version)), "invalid plugin version")
    add(errors, isinstance(description, str) and 0 < len(description) <= 1024, "plugin description must be 1..1024 chars")
    add(errors, isinstance(author, dict) and isinstance(author.get("name"), str) and 0 < len(author["name"]) <= 120, "author.name is required")
    if isinstance(author, dict) and author.get("url") is not None:
        add(errors, https_url(author.get("url")), "author.url must be HTTPS")
    if manifest.get("homepage") is not None:
        add(errors, https_url(manifest.get("homepage")), "homepage must be HTTPS")

    skill_path = manifest.get("skills", "./skills/")
    add(errors, isinstance(skill_path, str) and skill_path.startswith("./") and skill_path[2:].rstrip("/") == "skills", "skills path must resolve to ./skills/")
    skills: list[str] = []
    skill_root = root / "skills"
    if skill_root.is_dir():
        for directory in sorted(p for p in skill_root.iterdir() if p.is_dir()):
            definition = directory / "SKILL.md"
            add(errors, definition.is_file(), f"skill missing SKILL.md: {directory.name}")
            if not definition.is_file():
                continue
            skill_name, skill_description = skill_metadata(definition)
            add(errors, skill_name == directory.name, f"skill name mismatch: {directory.name}")
            add(errors, isinstance(skill_description, str) and 0 < len(skill_description) <= 1024, f"skill description invalid: {directory.name}")
            body = definition.read_text(encoding="utf-8")
            end = body.find("\n---", 4)
            add(errors, end >= 0 and bool(body[end + 4:].strip()), f"skill body empty: {directory.name}")
            if isinstance(name, str) and skill_name:
                add(errors, len(f"{name}:{skill_name}") <= 64, f"combined plugin/skill identity too long: {directory.name}")
            skills.append(directory.name)
    add(errors, bool(skills), "plugin must include at least one skill")

    has_mcp = (root / ".mcp.json").exists() or (root / ".app.json").exists() or "mcpServers" in manifest or "apps" in manifest
    architecture = "hybrid" if has_mcp and skills else "MCP-backed" if has_mcp else "skills-only"

    interface = manifest.get("interface")
    add(errors, isinstance(interface, dict), "manifest interface is required")
    interface = interface if isinstance(interface, dict) else {}
    for field, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000), ("developerName", 80)):
        value = interface.get(field)
        add(errors, isinstance(value, str) and 0 < len(value) <= limit and "\n" not in value and "\r" not in value, f"interface.{field} invalid")
    add(errors, interface.get("category") in CATEGORIES, "unsupported interface.category")

    capabilities = interface.get("capabilities", [])
    add(errors, isinstance(capabilities, list) and len(capabilities) <= 20, "interface.capabilities invalid")
    if isinstance(capabilities, list):
        for item in capabilities:
            add(errors, isinstance(item, str) and 0 < len(item) <= 120 and "\n" not in item, f"invalid capability: {item!r}")

    prompts = interface.get("defaultPrompt", [])
    add(errors, isinstance(prompts, list) and len(prompts) <= 3, "interface.defaultPrompt invalid")
    normalized: set[str] = set()
    if isinstance(prompts, list):
        for prompt in prompts:
            valid = isinstance(prompt, str) and 0 < len(prompt) <= 128 and "\n" not in prompt and "\r" not in prompt and not re.search(r"(?<![A-Za-z0-9._%+-])@[A-Za-z0-9_-]+", prompt)
            add(errors, bool(valid), f"invalid default prompt: {prompt!r}")
            if isinstance(prompt, str):
                key = " ".join(unicodedata.normalize("NFKC", prompt).split()).casefold()
                add(errors, key not in normalized, "duplicate normalized default prompt")
                normalized.add(key)

    for field, bg in (("brandColor", "#FFFFFF"), ("brandColorDark", "#212121")):
        value = interface.get(field)
        if value is not None:
            add(errors, isinstance(value, str) and bool(HEX.fullmatch(value)), f"interface.{field} must be six-digit hex")
            if isinstance(value, str) and HEX.fullmatch(value):
                add(errors, contrast(value, bg) >= 2.0, f"interface.{field} contrast is below 2:1")

    for field in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL", "supportURL"):
        value = interface.get(field)
        if value is not None:
            add(errors, https_url(value) and len(value) <= 1024, f"interface.{field} must be an HTTPS URL <=1024 chars")

    for field in ("logo", "composerIcon"):
        value = interface.get(field)
        add(errors, isinstance(value, str) and value.startswith("./"), f"interface.{field} must be a ./-relative path")
        if isinstance(value, str) and value.startswith("./"):
            path = (root / value[2:]).resolve()
            try:
                path.relative_to(root)
                inside = True
            except ValueError:
                inside = False
            add(errors, inside and path.is_file(), f"interface.{field} asset missing or outside root")
            if inside and path.is_file():
                add(errors, path.stat().st_size <= MAX_IMAGE, f"interface.{field} exceeds 5 MiB")
                add(errors, path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}, f"interface.{field} format unsupported")
                if path.suffix.lower() == ".svg":
                    validate_svg(path, f"interface.{field}", errors)

    files = 0
    dirs = 0
    total = 0
    normalized_paths: dict[str, str] = {}
    absolute_user = re.compile(r"/(?:Users|home)/[A-Za-z0-9._-]+/")
    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        for d in list(dirnames):
            path = current_path / d
            dirs += 1
            if d == "__pycache__" or path.is_symlink():
                errors.append(f"transient or symlink directory not allowed: {path.relative_to(root)}")
        for filename in filenames:
            path = current_path / filename
            rel = path.relative_to(root).as_posix()
            files += 1
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                errors.append(f"unreadable member: {rel}: {exc}")
                continue
            add(errors, stat.S_ISREG(mode) and not stat.S_ISLNK(mode), f"unsupported member type: {rel}")
            size = path.stat().st_size
            total += size
            add(errors, size <= MAX_MEMBER, f"member exceeds 100 MiB: {rel}")
            add(errors, filename not in {".DS_Store", "Thumbs.db"} and not filename.startswith("._"), f"OS metadata not allowed: {rel}")
            add(errors, path.suffix.lower() not in {".pyc", ".pyo"}, f"bytecode not allowed: {rel}")
            add(errors, not SECRET_BASENAME.match(filename), f"secret-shaped file not allowed: {rel}")
            key = unicodedata.normalize("NFC", rel).casefold()
            add(errors, key not in normalized_paths or normalized_paths[key] == rel, f"path normalization collision: {rel}")
            normalized_paths[key] = rel
            if size <= 1024 * 1024 and path.suffix.lower() in TEXT_SUFFIXES:
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    text = ""
                add(errors, not absolute_user.search(text), f"absolute user path found in public text: {rel}")

    add(errors, files + dirs <= MAX_ENTRIES, f"plugin exceeds {MAX_ENTRIES} entries")
    add(errors, total <= MAX_TOTAL, "plugin extracted size exceeds 512 MiB")
    add(errors, not (root / "hooks" / "hooks.json").exists(), "unexpected executable lifecycle hooks")

    return {
        "ok": not errors,
        "pluginRoot": str(root),
        "name": name if isinstance(name, str) else "",
        "version": version if isinstance(version, str) else "",
        "architecture": architecture,
        "skills": skills,
        "entries": files + dirs,
        "uncompressedBytes": total,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Marketing Council OpenAI plugin package.")
    parser.add_argument("plugin_root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate_plugin(args.plugin_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("plugin preflight: " + ("PASS" if report["ok"] else "FAIL"))
        print(f"architecture: {report['architecture']}; skills: {len(report['skills'])}; entries: {report['entries']}")
        for error in report["errors"]:
            print(f"error: {error}", file=sys.stderr)
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
