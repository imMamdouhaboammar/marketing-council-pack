# Pre-Mortem

Assume the recommendation failed by the decision horizon.

List the 3 to 5 most plausible causes, emphasizing hidden assumptions, distribution, product readiness, economics, creative requirements, execution capacity, measurement failure, competitive response, and customer behavior.

For each cause, name an early warning signal and a mitigation or stop rule.

## Emits

- `failure-risk-high` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
