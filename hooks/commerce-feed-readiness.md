# Commerce Feed Readiness

Trigger when product data cannot answer suitability, compatibility, comparison, use-case, inventory, price, or policy questions required by conversational or agent-mediated commerce.

## Emits

- `product-feed-poor` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
