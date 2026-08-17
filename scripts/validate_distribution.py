#!/usr/bin/env python3
"""Validate Marketing Council host-distribution metadata and component counts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXPECTED_NAME = "marketing-council"
EXPECTED_SKILLS = 29
EXPECTED_AGENTS = 24
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def fail(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def frontmatter_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or text.count("---") < 2:
        return ""
    return text.split("---", 2)[1]


def openai_interface(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(("display_name:", "short_description:", "default_prompt:")):
            key, value = stripped.split(":", 1)
            data[key] = value.strip().strip('"')
    return data


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = root / "manifest.json"
    fail(errors, manifest_path.exists(), "missing manifest.json")
    if not manifest_path.exists():
        return {"valid": False, "errors": errors, "warnings": warnings, "skill_count": 0, "agent_count": 0}

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest.get("version", "")
    fail(errors, manifest.get("name") == EXPECTED_NAME, "manifest name must be marketing-council")
    fail(errors, bool(re.fullmatch(r"\d+\.\d+\.\d+", version)), "manifest version must be strict semver")

    skills = sorted((root / "skills").glob("*/SKILL.md"))
    agents = sorted((root / "agents").glob("*.md"))
    fail(errors, len(skills) == EXPECTED_SKILLS, f"expected {EXPECTED_SKILLS} skills, found {len(skills)}")
    fail(errors, len(agents) == EXPECTED_AGENTS, f"expected {EXPECTED_AGENTS} agents, found {len(agents)}")

    for skill in skills:
        fm = frontmatter_text(skill)
        top_keys = []
        for line in fm.splitlines():
            if line and not line.startswith(" ") and ":" in line:
                top_keys.append(line.split(":", 1)[0].strip())
        fail(errors, set(top_keys) == {"name", "description"}, f"unsupported SKILL.md frontmatter: {skill.parent.name}: {top_keys}")

        metadata = skill.parent / "agents" / "openai.yaml"
        fail(errors, metadata.exists(), f"missing OpenAI metadata: {skill.parent.name}")
        if metadata.exists():
            iface = openai_interface(metadata)
            fail(errors, bool(iface.get("display_name")), f"missing OpenAI display_name: {skill.parent.name}")
            short = iface.get("short_description", "")
            fail(errors, 25 <= len(short) <= 64, f"OpenAI short_description must be 25..64 chars: {skill.parent.name}")
            prompt = iface.get("default_prompt", "")
            fail(errors, f"${skill.parent.name}" in prompt, f"OpenAI default_prompt must mention ${skill.parent.name}")

    for agent in agents:
        fm = frontmatter_text(agent)
        fail(errors, f"name: {agent.stem}" in fm, f"agent name mismatch: {agent.name}")
        fail(errors, "description: Use when" in fm, f"agent trigger description missing: {agent.name}")

    openai_path = root / ".codex-plugin" / "plugin.json"
    claude_path = root / ".claude-plugin" / "plugin.json"
    claude_market_path = root / ".claude-plugin" / "marketplace.json"
    openai_market_path = root / ".agents" / "plugins" / "marketplace.json"
    for path in (openai_path, claude_path, claude_market_path, openai_market_path):
        fail(errors, path.exists(), f"missing distribution metadata: {path.relative_to(root)}")

    if openai_path.exists():
        data = json.loads(openai_path.read_text(encoding="utf-8"))
        iface = data.get("interface", {})
        fail(errors, data.get("name") == EXPECTED_NAME, "OpenAI plugin name mismatch")
        fail(errors, data.get("version") == version, "OpenAI plugin version mismatch")
        fail(errors, data.get("skills") == "./skills/", "OpenAI plugin skills path must be ./skills/")
        fail(errors, len(iface.get("displayName", "")) <= 30, "OpenAI displayName exceeds 30 chars")
        fail(errors, 0 < len(iface.get("shortDescription", "")) <= 30, "OpenAI shortDescription must be 1..30 chars")
        fail(errors, len(iface.get("capabilities", [])) <= 20, "OpenAI capabilities exceeds 20")
        fail(errors, len(iface.get("defaultPrompt", [])) <= 3, "OpenAI defaultPrompt exceeds 3")
        for prompt in iface.get("defaultPrompt", []):
            fail(errors, len(prompt) <= 128 and "@" not in prompt and "\n" not in prompt, f"invalid OpenAI default prompt: {prompt}")
        for key in ("logo", "composerIcon"):
            value = iface.get(key, "")
            fail(errors, value.startswith("./"), f"OpenAI {key} must be ./-relative")
            fail(errors, (root / value.removeprefix("./")).exists(), f"missing OpenAI {key} asset")
        for key in ("brandColor", "brandColorDark"):
            if key in iface:
                fail(errors, bool(HEX.fullmatch(iface[key])), f"invalid OpenAI {key}")

    if claude_path.exists():
        data = json.loads(claude_path.read_text(encoding="utf-8"))
        fail(errors, data.get("name") == EXPECTED_NAME, "Claude plugin name mismatch")
        fail(errors, data.get("version") == version, "Claude plugin version mismatch")
        fail(errors, data.get("skills") == "./skills/", "Claude skills path mismatch")
        fail(errors, data.get("agents") == "./agents/", "Claude agents path mismatch")

    if claude_market_path.exists():
        data = json.loads(claude_market_path.read_text(encoding="utf-8"))
        fail(errors, data.get("name") == EXPECTED_NAME, "Claude marketplace name mismatch")
        entries = data.get("plugins", [])
        fail(errors, len(entries) == 1 and entries[0].get("name") == EXPECTED_NAME, "Claude marketplace plugin entry mismatch")

    if openai_market_path.exists():
        data = json.loads(openai_market_path.read_text(encoding="utf-8"))
        entries = data.get("plugins", [])
        fail(errors, len(entries) == 1 and entries[0].get("name") == EXPECTED_NAME, "OpenAI marketplace plugin entry mismatch")
        if entries:
            policy = entries[0].get("policy", {})
            fail(errors, bool(policy.get("installation")), "OpenAI marketplace installation policy missing")
            fail(errors, bool(policy.get("authentication")), "OpenAI marketplace authentication policy missing")
            fail(errors, bool(entries[0].get("category")), "OpenAI marketplace category missing")

    fail(errors, not (root / "hooks" / "hooks.json").exists(), "unexpected executable lifecycle hooks in public skills-only package")
    fail(errors, not (root / ".mcp.json").exists(), "unexpected MCP server in skills-only package")

    return {
        "valid": not errors,
        "name": manifest.get("name"),
        "version": version,
        "skill_count": len(skills),
        "agent_count": len(agents),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Marketing Council distribution metadata.")
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = validate(args.root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"valid={result['valid']} skills={result['skill_count']} agents={result['agent_count']}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
