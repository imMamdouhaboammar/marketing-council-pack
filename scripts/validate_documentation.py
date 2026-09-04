#!/usr/bin/env python3
"""Validate documentation lifecycle metadata, registry coverage, and internal links."""
from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "document-registry.json"
ALLOWED = {
    "ACTIVE",
    "ONGOING",
    "HISTORICAL_COMPLETED",
    "HISTORICAL_SUPERSEDED",
    "REFERENCE",
    "DEPRECATED",
}
ONGOING_FIELDS = (
    "Status",
    "Current state",
    "Completed work",
    "Remaining work",
    "Blockers",
    "Next verification step",
    "Source-of-truth references",
    "Last reviewed date",
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
METADATA_RE = re.compile(r"<!--\s*(.*?)\s*-->", re.DOTALL)


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def valid_review_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        return False
    return parsed.isoformat() == value


def parse_document_metadata(text: str) -> dict[str, str]:
    match = METADATA_RE.search(text)
    if not match:
        return {}
    metadata: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def review_date_errors(item: dict, metadata: dict[str, str]) -> list[str]:
    rel = item.get("path")
    registry_date = item.get("last_reviewed")
    document_date = metadata.get("last_reviewed")
    errors: list[str] = []
    if not valid_review_date(registry_date):
        errors.append(f"{rel}: registry last_reviewed must be a valid ISO date")
    if not valid_review_date(document_date):
        errors.append(f"{rel}: document last_reviewed must be a valid ISO date")
    if valid_review_date(registry_date) and valid_review_date(document_date) and registry_date != document_date:
        errors.append(
            f"{rel}: registry last_reviewed {registry_date} does not match document metadata {document_date}"
        )
    return errors


def validate() -> dict:
    errors: list[str] = []
    if not REGISTRY.is_file():
        return {"ok": False, "document_count": 0, "errors": ["docs/document-registry.json missing"]}

    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "document_count": 0, "errors": [f"registry unreadable: {exc}"]}

    add(errors, payload.get("version") == 1, "registry version must be 1")
    add(errors, valid_review_date(payload.get("last_reviewed")), "registry last_reviewed must be a valid ISO date")
    documents = payload.get("documents", [])
    paths = [item.get("path") for item in documents]
    add(errors, len(paths) == len(set(paths)), "registry contains duplicate document paths")

    actual = {
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "docs").rglob("*.md")
    }
    add(errors, set(paths) == actual, f"registry/docs markdown mismatch: registry={sorted(paths)} actual={sorted(actual)}")

    for item in documents:
        rel = item.get("path")
        status = item.get("status")
        source = item.get("source_of_truth")
        add(errors, status in ALLOWED, f"{rel}: invalid status {status!r}")
        add(errors, isinstance(source, bool), f"{rel}: source_of_truth must be boolean")
        if not isinstance(rel, str):
            continue
        path = ROOT / rel
        add(errors, path.is_file(), f"{rel}: document missing")
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        metadata = parse_document_metadata(text)
        errors.extend(review_date_errors(item, metadata))
        add(errors, f"doc_status: {status}" in text, f"{rel}: doc_status metadata mismatch")
        add(errors, f"source_of_truth: {str(source).lower()}" in text, f"{rel}: source_of_truth metadata mismatch")

        if isinstance(status, str) and status.startswith("HISTORICAL_"):
            add(errors, source is False, f"{rel}: historical document cannot be source of truth")
            add(errors, "Current source of truth" in text, f"{rel}: historical document must identify current source of truth")

        if status == "HISTORICAL_SUPERSEDED":
            replacements = item.get("superseded_by", [])
            add(errors, bool(replacements), f"{rel}: superseded document requires superseded_by")
            add(errors, "Do not execute this" in text, f"{rel}: superseded document requires execution warning")
            for replacement in replacements:
                add(errors, (ROOT / replacement).is_file(), f"{rel}: superseded_by target missing: {replacement}")

        if status == "ONGOING":
            for field in ONGOING_FIELDS:
                add(errors, field in text, f"{rel}: ongoing document missing {field}")

        for raw in LINK_RE.findall(text):
            target = raw.split("#", 1)[0]
            if not target or "://" in target or target.startswith("#"):
                continue
            resolved = (path.parent / target).resolve()
            add(errors, resolved.is_file() or resolved.is_dir(), f"{rel}: broken relative link {raw}")

    index = ROOT / "docs" / "README.md"
    if index.is_file():
        text = index.read_text(encoding="utf-8")
        for heading in (
            "Start here",
            "Current product documentation",
            "Ongoing work",
            "Architecture and contracts",
            "Release and distribution",
            "Historical specs",
            "Historical implementation plans",
        ):
            add(errors, heading in text, f"docs/README.md missing section: {heading}")

    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = manifest.get("version")
    release_doc = ROOT / "docs" / "OPENAI_RELEASE.md"
    add(errors, isinstance(version, str) and bool(version), "plugin version missing")
    if release_doc.is_file() and isinstance(version, str):
        release_text = release_doc.read_text(encoding="utf-8")
        add(errors, version in release_text, f"docs/OPENAI_RELEASE.md must reference current version {version}")

    submission = ROOT / "submission" / "README.md"
    if submission.is_file():
        submission_text = submission.read_text(encoding="utf-8")
        submission_metadata = parse_document_metadata(submission_text)
        add(errors, "doc_status: ONGOING" in submission_text, "submission/README.md must be ONGOING")
        add(errors, "source_of_truth: false" in submission_text, "submission/README.md cannot be source of truth")
        add(
            errors,
            valid_review_date(submission_metadata.get("last_reviewed")),
            "submission/README.md last_reviewed must be a valid ISO date",
        )
        for field in ONGOING_FIELDS:
            add(errors, field in submission_text, f"submission/README.md missing {field}")

    valid_item_dates = [
        item.get("last_reviewed")
        for item in documents
        if valid_review_date(item.get("last_reviewed"))
    ]
    if valid_item_dates and valid_review_date(payload.get("last_reviewed")):
        add(
            errors,
            payload.get("last_reviewed") == max(valid_item_dates),
            "registry top-level last_reviewed must match the latest managed document review date",
        )

    return {
        "ok": not errors,
        "document_count": len(documents),
        "current_release": version,
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Marketing Council documentation lifecycle.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("documentation lifecycle: " + ("PASS" if report["ok"] else "FAIL"))
        for error in report["errors"]:
            print(f"error: {error}")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
