# Evidence Gate

For every load-bearing claim, classify it as FACT, EVIDENCE, INFERENCE, ASSUMPTION, HYPOTHESIS, or UNKNOWN.

Fail the gate when:
- customer psychology is asserted without customer evidence
- market or competitor facts are stated without current verification when freshness matters
- attribution is described as causation without experimental or strong causal evidence
- an assumption materially affects the recommendation but is hidden

If evidence is weak, lower confidence and define what evidence should be collected next.

## Emits

- `evidence-quality-low` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
