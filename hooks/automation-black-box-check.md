# Automation Black Box Check

Trigger when a platform can make material decisions but explanations, logs, controls, or rollback paths are insufficient for the business risk.

## Emits

- `manual-control-low` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
