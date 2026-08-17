# AI Surface Check

Trigger when the buyer path may include AI answers, conversational search, or recommendation surfaces. Identify which surface changes the decision and require current evidence before prescribing platform-specific work.

## Emits

- `answer-surface-visibility-low` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run routing after the signal is added; do not force the same specialist set.
- Load the matching `references/2026/` card when a current platform capability is part of the recommendation.
- Preserve commercial, causal, customer, and brand counterweights activated by the graph.
