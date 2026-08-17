# Strategy Before Tactics

Trigger when a tactic is requested but the business problem, audience, objective, or constraints are unclear enough that the tactic could be wrong.

1. Identify the decision the tactic is supposed to support.
2. If existing context already supplies diagnosis, proceed without interrogation.
3. If one or two missing assumptions can be safely stated, label them and proceed.
4. If missing context could reverse the recommendation, perform lightweight diagnosis or research first.
5. Do not turn every small execution request into a strategy workshop.

## Emits

- `diagnosis-missing` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
