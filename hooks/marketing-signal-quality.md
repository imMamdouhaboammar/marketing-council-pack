# Marketing Signal Quality

Trigger when optimization is steered by weak proxy events, incomplete CRM outcomes, long latency, biased labels, or missing business-value signals.

## Emits

- `crm-signal-poor` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
