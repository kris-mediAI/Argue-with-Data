# P3 · Gemma agents

> You decide what to test and explain what the results mean. You never compute a number and never pick a verdict label.

**Owns:** `agents/`, `prompts/`, `fixtures/contracts/`, `fixtures/llm_cache/`, `tests/test_agents.py` · **Branch:** `p3-agents`
**Read first:** [PLAN.md](PLAN.md), `models/schemas.py`, [AGENTS.md](../../AGENTS.md)

## First 20 minutes: the biggest risk

Confirm Gemma returns valid structured JSON through `google-genai` with your `GEMINI_API_KEY` and `GEMMA_MODEL`:

1. **Try schema mode first:** `config={"response_mime_type": "application/json", "response_schema": Intent}`.
2. **If the Gemma model rejects that**, ask for JSON in the prompt, extract the first `{...}` block from the text, and validate it with `Intent.model_validate_json`. Retry once with the validation error.

Tell the team which approach works. Use hosted Gemma through the API, not a local model, because the deployed app has to reach it.

Then write `fixtures/contracts/hero.json`, the contracts you'd expect for the hero question. P4 builds against it.

## Agents (by 3:00)

| File | Function | Output |
|---|---|---|
| `agents/llm.py` | `call(prompt, schema)` | one wrapper: retry, then cache every response in `fixtures/llm_cache/` (`REPLAY=1` reads from it only) |
| `agents/analyst.py` | `parse_question(question, profile)` | `Intent` (periods, metric, the user's theory). No numbers. |
| `agents/hypothesis_generator.py` | `generate_hypotheses(profile, intent, baseline)` | 3–5 `Hypothesis` using only columns that exist. Always include the user's theory, data quality and seasonality. |
| `agents/planner.py` | `plan_tests(hypotheses, TOOL_SPECS)` | one `Contract` each. Clamp `support_at_least` to 0.25–0.60 in code, and drop any contract whose tool isn't in the registry. |
| `agents/critic.py` | `critique(verdicts, evidence)` | `CriticDecision`: alternative explanations and up to 2 follow-up contracts, e.g. a `drilldown` of Premium by customer. **No labels.** |
| `agents/synthesizer.py` | `synthesize(...)` | `Report`. Python formats every number first (`"₹2.06M"`, `"8%"`), and Gemma may only copy them. Say "accounts for", never "caused". |

Prompts go in `prompts/` as plain strings. Send the profile and computed numbers, never raw rows.

## Watch out for

- The free-form `args: dict` field in `Contract` may not work with schema mode. If so, have Gemma fill `args_json: str` and parse it in code.
- Save every rehearsal's responses in the cache. That's the fallback if the API fails during judging.

## On stage

You answer "What does the AI actually do?"
