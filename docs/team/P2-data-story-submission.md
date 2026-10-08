# P2 · Data, story and submission

> You build the trap dataset and own everything the judges see outside the app: README, demo video, Devpost and the pitch.

**Owns:** `data/`, `scripts/`, `README.md`, the demo video, the Devpost page · **Branch:** `p2-data`
**Read first:** [PLAN.md](PLAN.md), `models/schemas.py`, [AGENTS.md](../../AGENTS.md)

## The demo dataset (by 1:00; everyone is waiting on it)

`scripts/generate_data.py`, seeded, writes `data/demo_sales.csv` and `data/answer_key.json`.

- Columns: `date, order_id, customer, product, region, units, price, revenue`
- Jan–Mar 2026 only, so seasonality is UNTESTABLE.
- Feb about ₹10.0M, Mar about ₹7.94M (−20.6%).
- The product-mix shift (customers moving from Premium to cheaper products) accounts for about two-thirds of the decline, **spread across 30+ customers**.
- Customer X (fictional name): a top-3 account that orders weekly in Jan–Feb and places **zero orders in March**. About 8% of the decline, yet the **biggest single-customer drop**. That's the decoy.
- One region contributes about 14%. No missing days or duplicates.
- Compute `answer_key.json` with plain pandas inside the generator, **independently of P1's code**.
- Then a second preset, `--preset churn`, where churn really is the cause. It's for the live switch that shows the answer isn't hardcoded.

## The plain-AI test (by 1:30)

Ask plain Gemma or Gemini and ChatGPT "Why did revenue fall in March?" with the CSV attached. Screenshot the answers. If they don't blame Customer X, make the decoy more tempting.

## Submission (start at 2:00, finish by 5:00)

- **README.md** in the Hack Day template's format, which is already in place. Fill it in as features actually work. AGENTS.md forbids made-up results, so leave anything unfinished as a placeholder or mark it as not done.
- **Team names and contributions:** collect them from everyone.
- **AI usage:** Gemma in the app, plus every AI coding tool each person used (Codex, Claude Code, ...).
- **Challenges and learnings:** collect one from each person at the freeze.
- **License:** agree on one (MIT is typical) and add a `LICENSE` file.
- **Demo video** at 4:00–4:30. Say the event name at the start. Keep it to about 2 minutes.
- **Devpost:** project page, links to the repo, live app and video, team members.
- Make sure the repo is **public**.

## Demo script (under 3 minutes)

| Time | Beat |
|---|---|
| 0:00 | "AI is very good at finding plausible explanations. It's much worse at questioning them." |
| 0:15 | Plain-AI screenshot: it blames Customer X. |
| 0:30 | Upload the data, ask the question, enter the theory "I think it's Customer X." |
| 0:45 | Contracts lock on screen. Customer X → **WEAKENED**. Pause here. |
| 1:15 | Product mix → **SUPPORTED**. |
| 1:35 | Seasonality → **UNTESTABLE**. "It also knows when it doesn't have enough evidence." |
| 1:50 | Switch to the churn dataset: churn is now SUPPORTED. |
| 2:15 | "LLM proposes. Code tests. Critic challenges. Evidence decides." |

## On stage

You pitch and narrate.
