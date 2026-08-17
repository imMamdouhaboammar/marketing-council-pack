# Incrementality Required

Trigger when the question is causal: what marketing created, what spend to cut, what channel is incremental, or whether reported ROAS represents new business impact.

## Emits

- `incrementality-unknown` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
