# Freshness Check

Before relying on information that can change, verify it with current tools when available.

Treat these as freshness-sensitive: competitor prices and offers, platform features and policies, media costs, regulations, market availability, benchmarks, current trends, company roles, product versions, and vendor capabilities.

If current verification is unavailable, label the claim as UNKNOWN or ASSUMPTION rather than silently relying on memory.

## Emits

- `freshness-risk-high` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
