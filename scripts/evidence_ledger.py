#!/usr/bin/env python3
"""Inspect evidence-policy completeness across every Skill contract."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    registry=json.loads((ROOT/"routing"/"skill-contracts.json").read_text(encoding="utf-8")); rows=[]; errors=[]
    for slug in sorted(registry["contracts"]):
        path=ROOT/"skills"/slug/"references"/"skill-spec.json"
        if not path.is_file(): errors.append(f"{slug}: missing spec"); continue
        policy=json.loads(path.read_text(encoding="utf-8")).get("evidence_policy",{}); row={"skill":slug,"priority_levels":len(policy.get("priority",[])),"status_labels":policy.get("status_labels",[]),"freshness":bool(policy.get("freshness"))}; rows.append(row)
        if row["priority_levels"]<3 or len(row["status_labels"])<4 or not row["freshness"]: errors.append(f"{slug}: incomplete evidence policy")
    print(json.dumps({"ok":not errors,"skills":len(rows),"errors":errors,"ledger":rows},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
