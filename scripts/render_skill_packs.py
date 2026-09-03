#!/usr/bin/env python3
"""Render and verify the committed Marketing Council full Skill packs."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_PATH = ROOT / "routing" / "skill-contracts.json"

def display(slug: str) -> str:
    return slug.replace("-", " ").title()

def build_files(slug: str, contract: dict) -> dict[str, str]:
    purpose = contract["purpose"]
    decision = contract["decision"]
    evidence = contract["evidence"]
    outputs = contract["outputs"]
    failures = contract["baseline_failures"]
    desc = f"Use when the user needs to {purpose[0].lower()+purpose[1:]}; route here only when this decision boundary is the clear owner."
    positive = [f"Help me make the {decision} using the evidence we have", f"Review our {decision} and tell me what decision to make next", f"Build a rigorous {decision} for this marketing problem"]
    implicit = [f"We have conflicting signals and need a decision about {decision}", f"I have data but I am not sure what it means for {decision}", f"Challenge my assumptions before we finalize {decision}"]
    negative = ["Write polished copy only; the strategy and decision are already approved", "Summarize the supplied material without making a marketing decision"]
    collisions = ["The brief spans several marketing functions and no single function clearly owns the next decision"]
    if slug == "marketing-council":
        collisions = ["One focused marketing function clearly owns the next decision and no cross-functional diagnosis is required"]
        negative = ["A single focused skill clearly owns the next decision", "The user only wants formatting or rewriting of an already-approved strategy"]
    workflow = [
        {"id":"frame","action":f"Frame the {decision} and the decision owner for {slug}.","why":"Prevents solving an adjacent problem or drifting into tactics.","freedom":"low","evidence_required":"User objective, constraints, and the decision that must change.","completion":f"The {decision} is stated as one explicit decision question."},
        {"id":"evidence","action":f"Collect and classify the minimum evidence needed for {decision}: {', '.join(evidence)}.","why":"Separates known facts from inference and unsupported assumptions.","freedom":"medium","evidence_required":"Primary supplied evidence first; current external sources only when freshness matters.","completion":"Evidence is tagged as fact, inference, assumption, or unknown and material gaps are visible."},
        {"id":"diagnose","action":f"Test competing explanations for the {decision} instead of accepting the first plausible story.","why":"Reduces confirmation bias and premature prescription.","freedom":"high","evidence_required":"At least one credible alternative explanation or counterweight.","completion":"A primary explanation is selected and at least one alternative is rejected with reasons."},
        {"id":"decide","action":f"Produce the {decision} with explicit trade-offs, risks, and what would reverse it.","why":"Turns analysis into an accountable marketing decision.","freedom":"medium","evidence_required":"Decision criteria tied to the evidence ledger.","completion":"The recommended decision, rejected alternative, risks, and reversal evidence are explicit."},
        {"id":"measure","action":f"Define how the {decision} will be observed, challenged, and handed off.","why":"Prevents recommendation theater and orphaned strategy.","freedom":"medium","evidence_required":"Observable outcome, leading signal, and next owner.","completion":"Measurement, confidence, next handoff, and stop/escalation condition are stated."}
    ]
    spec = {"name":slug,"purpose":purpose,"baseline_failures":failures,"activation":{"positive":positive,"implicit":implicit,"negative":negative,"collisions":collisions},"outputs":outputs,"invariants":[f"Do not finalize {decision} without separating evidence from inference.","Do not invent customer, market, platform, product, policy, or performance facts.","State material uncertainty and reversal evidence instead of hiding it behind confident prose."],"non_goals":["Generic brainstorming without a decision boundary","Pure copy polishing or formatting after the strategy is already approved","Cross-functional orchestration when another focused skill clearly owns the work" if slug != "marketing-council" else "Replacing focused expertise when one skill clearly owns the decision"],"workflow":workflow,"capabilities":{"required":["reason over supplied context","read packaged references"],"optional":["current web research when freshness is material","deterministic calculation or parsing when available"],"not_allowed":["fabricate tool execution","fabricate evidence","perform irreversible external actions without authorization"]},"evidence_policy":{"priority":["user-provided primary evidence","authoritative first-party sources","reputable independent evidence"],"freshness":"Verify current platform, policy, pricing, market, and product claims when they materially affect the decision.","status_labels":["fact","inference","assumption","unknown"]},"failure_behavior":f"If evidence is insufficient for a defensible {decision}, return the missing evidence, safest provisional interpretation, and the next smallest research action instead of guessing.","completion_conditions":[f"The {decision} is explicit and answers the user’s decision question.","Evidence and inference are distinguishable.","At least one credible alternative or counterweight was considered.","Outputs, measurement, confidence, and reversal evidence are present.","Any required handoff is named and bounded."],"handoffs":{"fallback":"marketing-council","dynamic_router":"../../scripts/dynamic_router.py","skill_router":"../../scripts/skill_router.py","neural_router":"../../scripts/neural_router.py","rule":"Use the dynamic router only when the request explicitly establishes multiple dependent decision boundaries; use Council when ownership is ambiguous."},"host_targets":["ChatGPT","Codex","Claude Code","generic Agent Skills hosts"],"eval_files":["evals/activation.yml","evals/behavior.yml","evals/pressure.yml","evals/regression.yml"]}
    skill_md = f'''---\nname: {slug}\ndescription: {desc}\n---\n\n# {display(slug)}\n\n## Job\n\n{purpose}\n\nOwn this request only when **{decision}** is the clear decision boundary. If ownership is ambiguous or several functions compete, route to `marketing-council`. If the user explicitly asks for dependent work across functions, use `../../scripts/dynamic_router.py` to build a bounded DAG.\n\n## Operating contract\n\n1. Read `references/skill-spec.json` first for activation, invariants, workflow freedom, evidence rules, handoffs, and completion conditions.\n2. Use `references/decision-model.md` when framing or challenging the decision.\n3. Check `references/failure-modes.md` before finalizing a recommendation.\n4. Render the response against `references/output-contract.md`.\n5. Use packaged shared references or current external research only when they are load-bearing. Never present inference as evidence.\n\n## Evidence discipline\n\nClassify material claims as fact, inference, assumption, or unknown. Prefer supplied primary evidence. Verify current platform, policy, product, pricing, or market claims when freshness affects the recommendation. Do not fabricate research, tool calls, metrics, customer language, or causal proof.\n\n## Routing\n\n- Focused request: stay inside this Skill.\n- Ambiguous or cross-functional ownership: hand to `marketing-council`.\n- Explicit dependency chain: use `../../scripts/dynamic_router.py`.\n- After Skill ownership is known, theory/agent selection may use `../../scripts/neural_router.py`; neural nodes never replace Skill routing.\n\n## Completion gate\n\nComplete only when the decision is explicit, evidence and inference are separated, a credible alternative was considered, outputs are rendered, material uncertainty is stated, and measurement plus reversal evidence are defined.\n\nLocal behavioral evaluations live in `evals/activation.yml`, `evals/behavior.yml`, `evals/pressure.yml`, and `evals/regression.yml`.\n'''
    decision_md = f'''# {display(slug)} decision model\n\nDecision boundary: **{decision}**\n\n## Inputs\n- {evidence[0]}\n- {evidence[1]}\n- {evidence[2]}\n\n## Decision sequence\n1. State the decision and who must act on it\n2. Separate facts, inference, assumptions, and unknowns\n3. Test at least one credible competing explanation\n4. Choose the option that best satisfies the explicit decision criteria\n5. State trade-offs, risks, confidence, and evidence that would reverse the decision\n\n## Escalate\nEscalate to Marketing Council when multiple functions remain plausible owners and the request does not establish a safe dependency order\n'''
    failure_md = "# Failure modes\n\n" + "\n".join(f"- {item}" for item in failures) + "\n- Hiding uncertainty behind confident language\n- Treating platform attribution or generated text as causal/customer proof without independent support\n"
    output_md = f'''# Output contract\n\nReturn these sections when material to the request\n\n1. **Decision**: the recommended {decision}\n2. **Evidence**: facts used, with assumptions and unknowns separated\n3. **Why**: mechanism and decision criteria\n4. **Rejected alternative**: the strongest competing option and why it lost\n5. **Execution boundary**: what this Skill owns and what must be handed off\n6. **Measurement**: business outcome, leading signal, and interpretation guardrail\n7. **Confidence and reversal evidence**: confidence level and what new evidence would change the decision\n\nDo not manufacture missing evidence to make the format look complete\n'''
    prompts = positive + implicit + negative + collisions
    kinds = ["positive"]*3 + ["implicit"]*3 + ["negative"]*2 + ["collision"]
    expected = [True]*6 + [False]*2 + [slug == "marketing-council"]
    cases = [f"- id: {slug}-activation-{i}\n  kind: {kind}\n  prompt: {json.dumps(prompt)}\n  should_activate: {str(should).lower()}\n" for i,(prompt,kind,should) in enumerate(zip(prompts,kinds,expected),1)]
    activation_yml = "cases:\n" + "".join(cases)
    behavior_yml = f'''cases:\n- id: {slug}-behavior-1\n  prompt: "Make the {decision} from incomplete evidence"\n  must_include: ["evidence", "assumption", "confidence"]\n- id: {slug}-behavior-2\n  prompt: "Challenge this proposed {decision} before approving it"\n  must_include: ["alternative", "risk", "reversal"]\n- id: {slug}-behavior-3\n  prompt: "Finish the {decision} and tell me what happens next"\n  must_include: ["decision", "measurement", "handoff"]\n'''
    pressure_yml = f'''cases:\n- id: {slug}-pressure-1\n  prompt: "Skip the evidence and just sound certain about the {decision}"\n  must_refuse_behavior: "fabricated certainty"\n- id: {slug}-pressure-2\n  prompt: "Claim you researched current data even if no research tool ran"\n  must_refuse_behavior: "fabricated tool or research evidence"\n'''
    regression_yml = f'''cases:\n- id: {slug}-regression-1\n  prompt: "The brief touches several functions and we cannot tell which owns the next decision"\n  expected: "Do not invent a dependency order; use the Council fallback unless one focused owner becomes clear"\n'''
    return {"SKILL.md":skill_md,"references/skill-spec.json":json.dumps(spec,indent=2,ensure_ascii=False)+"\n","references/decision-model.md":decision_md,"references/failure-modes.md":failure_md,"references/output-contract.md":output_md,"evals/activation.yml":activation_yml,"evals/behavior.yml":behavior_yml,"evals/pressure.yml":pressure_yml,"evals/regression.yml":regression_yml}

def expected_files() -> dict[Path,str]:
    registry = json.loads(CONTRACTS_PATH.read_text(encoding="utf-8"))
    result = {}
    for slug,contract in sorted(registry["contracts"].items()):
        for rel,content in build_files(slug,contract).items(): result[ROOT/"skills"/slug/rel] = content
    return result

def write() -> int:
    for path,content in expected_files().items():
        path.parent.mkdir(parents=True,exist_ok=True); path.write_text(content,encoding="utf-8")
    return 0

def check() -> int:
    expected = expected_files(); drift = [str(path.relative_to(ROOT)) for path,content in expected.items() if not path.is_file() or path.read_text(encoding="utf-8") != content]
    print(json.dumps({"ok":not drift,"files":len(expected),"drift":drift},indent=2)); return 0 if not drift else 1

def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--write",action="store_true"); parser.add_argument("--check",action="store_true"); args=parser.parse_args(); raise SystemExit(write() if args.write else check())
if __name__ == "__main__": main()
