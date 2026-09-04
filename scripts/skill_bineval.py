#!/usr/bin/env python3
"""Deterministic structural BinEval for Marketing Council Skill packs."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def count_cases(path): return len(re.findall(r"^- id:\s*[a-z0-9-]+\s*$",path.read_text(encoding="utf-8"),re.M))
def evaluate(slug):
    root=ROOT/"skills"/slug; spec=json.loads((root/"references"/"skill-spec.json").read_text(encoding="utf-8")); counts={name:count_cases(root/"evals"/name) for name in ("activation.yml","behavior.yml","pressure.yml","regression.yml")}; activation=spec["activation"]
    dimensions={"activation_boundary":len(activation["positive"])>=3 and len(activation["implicit"])>=3 and len(activation["negative"])>=2,"collision_boundary":len(activation["collisions"])>=1,"workflow_contract":len(spec["workflow"])>=4 and all(step.get("completion") and step.get("evidence_required") for step in spec["workflow"]),"evidence_discipline":bool(spec["evidence_policy"]) and len(spec["invariants"])>=3,"pressure_resistance":counts["pressure.yml"]>=2,"regression_proof":counts["regression.yml"]>=1,"progressive_disclosure":len((root/"SKILL.md").read_text(encoding="utf-8").splitlines())<220}; score=round(100*sum(dimensions.values())/len(dimensions)); return {"skill":slug,"score":score,"dimensions":dimensions,"eval_cases":counts}
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--skill"); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); registry=json.loads((ROOT/"routing"/"skill-contracts.json").read_text(encoding="utf-8")); slugs=[args.skill] if args.skill else sorted(registry["contracts"]); results=[evaluate(slug) for slug in slugs]; ok=all(item["score"]==100 for item in results); payload={"ok":ok,"skills":len(results),"minimum_score":min(item["score"] for item in results),"results":results}; print(json.dumps(payload,indent=2)); return 0 if ok else 1
if __name__=="__main__": raise SystemExit(main())
