#!/usr/bin/env python3
"""Fail closed when committed Skill packs drift from the Omni-style contract."""
from __future__ import annotations
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REQUIRED=("SKILL.md","agents/openai.yaml","references/skill-spec.json","references/decision-model.md","references/failure-modes.md","references/output-contract.md","evals/activation.yml","evals/behavior.yml","evals/pressure.yml","evals/regression.yml")
SPEC_FIELDS=("name","purpose","baseline_failures","activation","outputs","invariants","non_goals","workflow","capabilities","evidence_policy","failure_behavior","completion_conditions","handoffs","host_targets","eval_files")
def case_count(path): return len(re.findall(r"^- id:\s*[a-z0-9-]+\s*$",path.read_text(encoding="utf-8"),re.M))
def main():
    registry=json.loads((ROOT/"routing"/"skill-contracts.json").read_text(encoding="utf-8")); slugs=sorted(registry["contracts"]); errors=[]
    if len(slugs)!=29: errors.append(f"expected 29 contracts, found {len(slugs)}")
    render=subprocess.run([sys.executable,str(ROOT/"scripts"/"render_skill_packs.py"),"--check"],capture_output=True,text=True)
    if render.returncode: errors.append("render drift: "+(render.stdout or render.stderr).strip())
    failure_fps=set(); workflow_fps=set()
    for slug in slugs:
        root=ROOT/"skills"/slug
        for rel in REQUIRED:
            if not (root/rel).is_file(): errors.append(f"{slug}: missing {rel}")
        path=root/"references"/"skill-spec.json"
        if not path.is_file(): continue
        spec=json.loads(path.read_text(encoding="utf-8"))
        for field in SPEC_FIELDS:
            if field not in spec: errors.append(f"{slug}: missing spec field {field}")
        if spec.get("name")!=slug: errors.append(f"{slug}: spec name mismatch")
        failure_fp=tuple(spec.get("baseline_failures",[])); workflow_fp=tuple(step.get("action") for step in spec.get("workflow",[]))
        if slug!="marketing-council":
            if failure_fp in failure_fps: errors.append(f"{slug}: cloned baseline failures")
            if workflow_fp in workflow_fps: errors.append(f"{slug}: cloned workflow")
            failure_fps.add(failure_fp); workflow_fps.add(workflow_fp)
        for name,minimum in {"activation.yml":9,"behavior.yml":3,"pressure.yml":2,"regression.yml":1}.items():
            ep=root/"evals"/name
            if ep.is_file() and case_count(ep)<minimum: errors.append(f"{slug}: {name} has fewer than {minimum} cases")
        text=(root/"SKILL.md").read_text(encoding="utf-8") if (root/"SKILL.md").is_file() else ""
        if len(text.splitlines())>=220: errors.append(f"{slug}: SKILL.md exceeds progressive-disclosure limit")
    print(json.dumps({"ok":not errors,"skills":len(slugs),"errors":errors},indent=2)); return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
