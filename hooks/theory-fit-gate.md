# Theory Fit Gate

Fail when a framework is selected because it is famous or familiar rather than because its mechanism matches the evidence. Require: observed constraint, theory mechanism, expected prediction, counterweight, and reversal evidence.

## Emits

- `theory-fit-low` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
