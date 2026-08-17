# Horizon Balance Check

Separate immediate response objectives from longer-horizon memory and market effects. Require metrics and decision dates that match each horizon.

## Emits

- `short-horizon` when supported by the diagnosis.
- `long-horizon` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
