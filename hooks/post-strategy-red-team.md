# Post-Strategy Red Team

Run after a significant strategy is drafted.

Attack:
- unsupported facts
- requested-channel bias
- vague differentiation
- correlation treated as causation
- vanity metrics
- ignored product or retention problems
- missing economics
- excessive complexity
- lack of exclusions
- lack of kill criteria

Return only findings that could materially change the recommendation, then revise the strategy where warranted.

## Emits

- `contradiction-risk-high` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
