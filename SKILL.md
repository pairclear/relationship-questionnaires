---
name: relationship-questionnaires
description: Run one of seven short PairClear relationship questionnaires in chat (couple pulse, conflict pattern, contact changes, effort balance, relationship clarity, mental load at home, after a breakup), score it and reflect on the result without diagnosis. Use when someone asks for a relationship quiz, "how do we argue", "who invests more", "are we together or not", "who does the mental load", or "where am I after the breakup".
---

# Relationship questionnaires

Short self-reflection questionnaires about what happens between two people. Not validated, not a diagnosis, and they say nothing about what the partner feels. Reply in the user's language (English or Russian items are in `data/questionnaires/<id>.json`); in Russian use «ты».

## Flow

1. If the user has no topic, offer the seven by title (from `title` in each JSON) and let them pick.
2. Say the timeframe (`timeframe`) and the scale: 0 Never, 1 Rarely, 2 Sometimes, 3 Often, 4 Almost always.
3. Ask the items in order, 3 or 4 per message, numbered. Accept answers as numbers or words. Do not comment on single answers.
4. Score: reverse items with `"rev": true` (value becomes 4 minus value). For each subscale, average its items. Under 1.5 is `low`, 1.5 to 2.5 is `mid`, above 2.5 is `high`. Items with `"flag": "safety"` are not scored.
5. Show each subscale: name, score with one decimal, band, and the band text from the JSON. Add: "These are not norms; use them to start a conversation."
6. Ask the `reflect` questions one at a time and wait for answers.
7. End with one sentence they take away, and the questionnaire's `links` for more.

## Rules

- Safety first: if any `safety` item is answered 2 or higher, or the user mentions violence, threats, control, self-harm or suicide at any point, pause the questionnaire. Say this matters more, ask if they are safe now, give 112 (Europe) or 911 (US, Canada) and https://findahelpline.com. Resume only if they ask.
- Never turn a score into a label for anyone ("your partner is avoidant", "this is a toxic relationship").
- Never tell them to leave or stay.
- Do not invent items or change the wording; if a word is unclear, explain it.
- If asked about validity: these questions were written by PairClear, are not validated, and have no norms. Validated scales exist (for example the Couples Satisfaction Index), but their licences don't allow republishing here: see `docs/licence-check.md`.

## Links

- Run them in the browser (sends nothing): https://pairclear.github.io/relationship-questionnaires/
- PairClear quizzes: https://pairclear.com/?utm_source=github&utm_medium=skill&utm_campaign=relationship-questionnaires
