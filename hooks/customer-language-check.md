# Customer Language Check

When writing strategy, messaging, offers, or content from customer insight, prefer observed language from interviews, sales calls, search queries, reviews, support tickets, CRM notes, comments, or surveys.

Do not manufacture quotes or claim that a phrase is "how customers speak" without evidence. Separate exact language from analyst paraphrase.

## Emits

- `customer-language-missing` when the gate condition is present.

## Neural connections

- Send emitted signals to `../neural/graph.json`.
- Re-run `../scripts/neural_router.py` when the signal could change specialist or theory selection.
