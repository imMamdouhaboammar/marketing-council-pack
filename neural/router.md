# Neural Router

The router is a deterministic activation helper. It does not replace diagnosis.

1. Run challenge hooks and collect supported signal IDs.
2. Pass signals to `scripts/neural_router.py`.
3. Load the highest-ranked agents, skills, theories, and principles that could materially change the decision.
4. Preserve explicit `counterbalances` edges during synthesis.
5. If evidence changes, re-run the router.

Example:

```bash
python scripts/neural_router.py --signals category-mature,differentiation-weak,competitor-pressure-high --json
```
