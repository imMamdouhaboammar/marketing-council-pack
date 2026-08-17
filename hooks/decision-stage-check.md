# Decision Stage Check

Classify the buyer decision state and awareness relevant to the current buying situation. Use it to change education depth, proof, directness, and CTA.

## Emits

- `awareness-low` when supported by the diagnosis.
- `awareness-high` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
