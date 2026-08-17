# Closed Loop Bias Check

Trigger when purchase data is observed inside a retailer, marketplace, or commerce platform and attributed sales are being treated as incremental impact without a counterfactual.

## Emits

- `commerce-media-bias-risk` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
