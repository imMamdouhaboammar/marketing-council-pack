# Automation Authority Check

Trigger before giving a marketing agent or platform authority to change spend, targeting, bids, creative, offers, or campaign structure. Require an explicit authority matrix and limits.

## Emits

- `automation-boundaries-unclear` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
