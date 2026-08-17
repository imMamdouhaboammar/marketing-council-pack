# Category Maturity Check

Classify whether the category is emerging, developing, mature, saturated, or unclear using evidence. Use the classification to change positioning, proof burden, media, and category strategy.

## Emits

- `category-mature` when supported by the diagnosis.
- `category-unclear` when supported by the diagnosis.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-route specialists and theories when the emitted signal changes the decision context.
- Preserve any `counterbalances` edge activated by the new signal.
