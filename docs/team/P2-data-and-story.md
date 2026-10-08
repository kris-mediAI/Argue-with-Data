# P2 · Data and story

> You build the trap dataset and own the pitch. In a 5-hour hackathon the demo is most of the score, so this role matters as much as the code.

**Owns:** `data/`, `scripts/`, `demo/`, `README.md`
**Read first:** [PLAN.md](PLAN.md) and `models/schemas.py`

## 0:00–1:00 · The hero dataset (everyone is waiting on it)

`scripts/generate.py`, seeded, writes `data/hero.csv` and `data/answer_key.json`.

- Columns: `date, order_id, customer, product, region, units, price, revenue`
- Jan–Mar 2026 only, so seasonality is UNTESTABLE.
- Feb about ₹10.2M, Mar about ₹8.1M (around −20%).
- Products Premium / Standard / Basic. The premium drop is about two-thirds of the decline and **spread across 30+ customers**.
- Customer X (a fictional name, no real companies): a top-3 account that orders every week in Jan–Feb and places **zero orders in March**. About 8% of the decline, but the **biggest drop of any single customer**. That's what makes it the tempting wrong answer.
- No region above about 25% of the decline. No missing days.
- Compute `answer_key.json` with plain pandas inside the generator, **independently of P1's code**: total change, each hypothesis's expected share, and expected verdict.

A rough version on time beats a polished one late. Tune it afterwards.

## 1:00–1:30 · The plain-AI test (the pitch depends on it)

Give `hero.csv` to plain Gemini and ChatGPT in fresh chats and ask *"Why did revenue fall in March?"* Screenshot the answers into `demo/`. If they don't blame Customer X, make the decoy more tempting and retest. Tell P3 the result either way.

## 1:30–3:30 · Second dataset and the pitch

- **Dataset A:** `--preset churn`. Five large customers stop ordering, about 60% of the decline. Customer churn should come out SUPPORTED. Switching to it live proves the answer isn't hardcoded.
- Optional if quick: **Dataset G**, 7 days of March missing, so data quality comes out SUPPORTED.
- `demo/script.md` and slides, if the hackathon wants them.

## Demo script (under 3 minutes)

| Time | Beat |
|---|---|
| 0:00 | "AI is very good at finding plausible explanations. It's much worse at questioning them." |
| 0:15 | Plain-AI screenshot: it blames Customer X. |
| 0:30 | Upload the hero data, ask the question, enter the theory "I think it's Customer X." |
| 0:45 | Contracts lock on screen. Customer X → **WEAKENED**. Pause here. |
| 1:15 | Product → **SUPPORTED**. |
| 1:35 | Seasonality → **UNTESTABLE**. "It also knows when it doesn't have enough evidence." |
| 1:50 | Switch to Dataset A: churn is now SUPPORTED. "The answer isn't hardcoded." |
| 2:15 | "The LLM proposes. Code tests. The critic challenges. Evidence decides." |

## 3:30–5:00

README (what it is, how to run it, one diagram), then run both rehearsals with a timer.

## On stage

You pitch and narrate.
