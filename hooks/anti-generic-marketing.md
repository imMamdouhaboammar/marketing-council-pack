# Anti-Generic Marketing

Reject recommendations that could be pasted unchanged into unrelated businesses.

Generic phrases such as "build awareness", "engage the audience", "create valuable content", "use social media", or "track KPIs" are incomplete unless the answer defines who, why, mechanism, message, channel role, measurement, and decision threshold.

Prefer fewer specific recommendations over a long inventory of activities.

## Emits

- `generic-tactic-risk` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
