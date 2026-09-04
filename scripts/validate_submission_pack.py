#!/usr/bin/env python3
"""Validate the evidence-bound Marketing Council OpenAI submission draft."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACK = ROOT / "submission" / "submission-pack.json"
EVIDENCE_REF = re.compile(
    r"^(tests/test_(?:skill|dynamic)_router\.py)::(test_[A-Za-z0-9_]+)$"
)
REQUIRED_MISSING = {
    "verified_developer_identity",
    "privacy_policy_url",
    "terms_of_service_url",
    "support_url",
    "country_or_region_availability",
}


def add(errors: list[str], condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def validate(pack_path: Path) -> dict:
    errors: list[str] = []
    pack_path = pack_path.resolve()
    if not pack_path.is_file():
        return {"ok": False, "errors": [f"submission pack missing: {pack_path}"]}

    try:
        pack = json.loads(pack_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"ok": False, "errors": [f"submission pack unreadable: {exc}"]}

    manifest = json.loads((ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    listing = json.loads((ROOT / "submission" / "listing.json").read_text(encoding="utf-8"))

    add(errors, pack.get("schema_version") == 1, "schema_version must be 1")
    add(errors, pack.get("artifact_use") == "SUBMISSION_DRAFT", "artifact_use must be SUBMISSION_DRAFT")
    add(errors, pack.get("submission_type") == "skills-only", "submission_type must be skills-only")
    add(errors, pack.get("pack_status") == "PARTIAL_MISSING_INPUT", "pack_status must remain PARTIAL_MISSING_INPUT until required external inputs exist")

    plugin = pack.get("plugin", {})
    add(errors, plugin.get("package_name") == "marketing-council", "plugin package_name mismatch")
    add(errors, plugin.get("version") == manifest.get("version") == listing.get("version"), "submission, manifest, and listing versions must match")
    add(errors, plugin.get("skill_count") == 29, "submission pack must report 29 total Skills")
    add(errors, plugin.get("focused_skill_count") == 28, "submission pack must report 28 focused Skills")
    add(errors, plugin.get("fallback_skill") == "marketing-council", "fallback Skill must be marketing-council")

    portal = pack.get("portal_state", {})
    for field in ("submitted", "reviewed", "approved", "published"):
        add(errors, portal.get(field) is False, f"portal_state.{field} must be false in the repository draft")

    missing = set(pack.get("missing_required_inputs", []))
    add(errors, missing == REQUIRED_MISSING, f"missing_required_inputs mismatch: {sorted(missing)}")

    cases = pack.get("review_cases", [])
    positive = [case for case in cases if case.get("kind") == "positive"]
    negative = [case for case in cases if case.get("kind") == "negative"]
    add(errors, len(cases) == 8, f"expected exactly 8 review cases, found {len(cases)}")
    add(errors, len(positive) == 5, f"expected exactly 5 positive cases, found {len(positive)}")
    add(errors, len(negative) == 3, f"expected exactly 3 negative cases, found {len(negative)}")

    ids: set[str] = set()
    prompts: set[str] = set()
    for index, case in enumerate(cases, 1):
        case_id = case.get("id")
        prompt = case.get("prompt")
        add(errors, isinstance(case_id, str) and bool(case_id), f"case {index}: id required")
        add(errors, isinstance(prompt, str) and bool(prompt.strip()), f"case {index}: prompt required")
        if isinstance(case_id, str):
            add(errors, case_id not in ids, f"duplicate case id: {case_id}")
            ids.add(case_id)
        if isinstance(prompt, str):
            normalized = " ".join(prompt.split()).casefold()
            add(errors, normalized not in prompts, f"duplicate case prompt: {case_id}")
            prompts.add(normalized)

        for field in ("expected_behavior", "expected_result_shape", "actual_result_summary"):
            add(errors, isinstance(case.get(field), str) and bool(case[field].strip()), f"{case_id}: {field} required")
        add(errors, case.get("evidence_kind") == "PASSED_TEST_EVIDENCE", f"{case_id}: evidence_kind must be PASSED_TEST_EVIDENCE")

        ref = case.get("evidence_reference")
        match = EVIDENCE_REF.fullmatch(ref) if isinstance(ref, str) else None
        add(errors, match is not None, f"{case_id}: invalid evidence_reference")
        if match:
            test_file = ROOT / match.group(1)
            test_name = match.group(2)
            add(errors, test_file.is_file(), f"{case_id}: evidence test file missing")
            if test_file.is_file():
                source = test_file.read_text(encoding="utf-8")
                add(errors, f"def {test_name}(" in source, f"{case_id}: evidence test function missing")

    boundary = pack.get("release_boundary", "")
    add(errors, "not performed" in boundary, "release boundary must say portal/publication actions were not performed")
    add(errors, "public ChatGPT/Codex publication" in boundary, "release boundary must distinguish public ChatGPT/Codex publication")

    notes = pack.get("release_notes", "")
    add(errors, "declared handoff" in notes, "release notes must mention declared handoff validation")
    add(errors, "symlink" in notes, "release notes must mention symlink hardening")
    add(errors, "29" in notes, "release notes must mention the 29-Skill inventory")

    ledger = pack.get("evidence_ledger", [])
    add(errors, bool(ledger), "evidence ledger must not be empty")
    allowed_statuses = {"CONFIRMED_PRODUCT_FACT", "PASSED_TEST_EVIDENCE", "PROPOSED_OR_UNVERIFIED"}
    for index, item in enumerate(ledger, 1):
        add(errors, item.get("status") in allowed_statuses, f"evidence ledger row {index}: unsupported status")

    return {
        "ok": not errors,
        "pack_status": pack.get("pack_status"),
        "version": plugin.get("version"),
        "positive_cases": len(positive),
        "negative_cases": len(negative),
        "missing_required_inputs": sorted(missing),
        "errors": errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Marketing Council submission draft.")
    parser.add_argument("pack", type=Path, nargs="?", default=DEFAULT_PACK)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = validate(args.pack)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("submission draft validation: " + ("PASS" if report["ok"] else "FAIL"))
        for error in report["errors"]:
            print(f"error: {error}")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
