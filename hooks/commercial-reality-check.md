# Commercial Reality Check

Before recommending scale, discounting, acquisition, or channel expansion, inspect the economics that can invalidate the idea.

Check as applicable: price, gross margin, variable costs, contribution margin, CAC definition, LTV definition, payback, refund/return rate, retention, sales capacity, fulfillment capacity, cash constraints, and marginal rather than average performance.

A tactic can be marketing-sensible and commercially wrong. Say so explicitly.

## Emits

- `economics-unhealthy` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
