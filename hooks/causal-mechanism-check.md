# Causal Mechanism Check

Require a plausible chain from tactic to behavior to commercial outcome. Fail when attribution, correlation, or engagement is treated as causation without sufficient evidence.

## Emits

- `causal-claim-weak` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
