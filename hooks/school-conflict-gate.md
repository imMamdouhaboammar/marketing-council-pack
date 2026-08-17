# School Conflict Gate

When two credible schools imply different actions, preserve the conflict. Require explicit deciding factors such as category maturity, growth horizon, economics, distribution, evidence quality, and reversibility.

## Emits

- `school-conflict-high` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
