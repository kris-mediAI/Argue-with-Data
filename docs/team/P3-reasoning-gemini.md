# P3 · Reasoning (Gemini)

> You decide what to test and explain what the results mean. You never compute a number and never pick a verdict label.

**Owns:** `llm/`, `fixtures/contracts/`, `tests/test_reasoning.py`
**Read first:** [PLAN.md](PLAN.md) and `models/schemas.py`

## 0:00–0:45 · Unblock P4

1. Get a Gemini key into `.env` and confirm one structured call works.
2. Hand-write `fixtures/contracts/hero.json`: the 5 contracts you'd expect for "Why did revenue fall in March?" on the hero data. P4 builds the UI from it.

## 0:45–3:00 · The Gemini calls

1. **`llm/gemini.py`**: one wrapper for every call, with structured output:
   ```python
   from google import genai
   client = genai.Client()   # reads GEMINI_API_KEY
   resp = client.models.generate_content(
       model=os.environ["GEMINI_MODEL"],
       contents=prompt,
       config={"response_mime_type": "application/json",
               "response_schema": Intent, "temperature": 0.2},
   )
   intent = resp.parsed
   ```
   Retry once on invalid output. **Save every response** to `llm/cache/<sha of prompt>.json`. With `REPLAY=1`, read only from the cache. That's the offline demo fallback, so commit the cache.
2. **`interpret(question, profile) -> Intent`**: metric, the two periods, and the user's theory if given. Put any guesses in `assumptions`. No numbers.
3. **`hypothesize(profile, intent, headline) -> list[Hypothesis]`**: 3–5 hypotheses using only columns that exist (check in code). Always include the user's theory (`source="user"`), data quality, and seasonality (the UNTESTABLE moment is part of the demo). Send the profile, never raw rows.
4. **`write_contracts(hypotheses, TOOL_SPECS) -> list[Contract]`**. Put P1's `TOOL_SPECS` in the prompt with these mappings as examples:

   | Hypothesis | Tool |
   |---|---|
   | Customer churn | `customer_bridge` |
   | A specific customer (user's theory) | `customer_bridge` with `focus` |
   | Product decline | `breakdown` with `dimension="product"` |
   | Regional decline | `breakdown` with `dimension="region"` |
   | Seasonality | `trend` |
   | Data problem | `data_quality` |

   Clamp `support_at_least` to 0.25–0.60 in code. Drop any contract whose tool isn't in `TOOL_REGISTRY`.
5. **`report(...) -> Report`** plus one rationale sentence per verdict. **Format every number in Python first** (`"₹2.1M"`, `"8%"`) and give the LLM the list to copy from. Say "accounts for", never "caused".

**By 3:00:** hand all four functions to P4, tested against P1's fixture Evidence.

## Watch out for

- Gemini's structured output may reject the free-form `args: dict` field. If it does, have the LLM fill an `args_json: str` field and parse it into a `Contract` in code.
- Rate limits: replay mode is your fallback, so cache every run you rehearse.

## 3:30–4:15 · Stretch, only if on schedule

**Critic:** after the verdicts, one call that asks "is the top explanation another one in disguise?" On the hero data it should request a `drilldown` of Premium by customer. The result (spread across 30+ customers) lets product mix survive the challenge. This is the moment a fixed checklist couldn't produce.

## On stage

You answer "What does the LLM actually do?" Point at a locked contract next to its result.
