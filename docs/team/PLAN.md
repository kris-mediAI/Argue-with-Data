# Team plan (5 hours)

**LLM proposes. Code tests. Critic challenges. Evidence decides.**

Argue With My Data investigates why a business metric changed. Gemini proposes competing explanations and writes a **falsification contract** for each one: which test runs, and which result would support or reject it. The contract is locked (timestamp + hash) before the test runs. Pandas computes the evidence, `judge()` compares it with the contract to assign a verdict, and Gemini writes the explanation using only computed numbers.

**The hero demo:** revenue fell about 20% from February to March. A plain AI blames Customer X, a big account that stopped ordering. We test it: Customer X accounts for about 8% of the decline → WEAKENED. The premium-product drop accounts for about two-thirds → SUPPORTED. Seasonality → UNTESTABLE (3 months of data). Exact figures come from `data/answer_key.json`.

**The goal for 5 hours:** one demo that works every time. Not a complete system.

## Roles

| | Role | Brief | Owns |
|---|---|---|---|
| P1 | Analysis engine | [P1-analysis-engine.md](P1-analysis-engine.md) | `analysis/`, `fixtures/evidence/` |
| P2 | Data and story | [P2-data-and-story.md](P2-data-and-story.md) | `data/`, `scripts/`, `demo/`, `README.md` |
| P3 | Reasoning (Gemini) | [P3-reasoning-gemini.md](P3-reasoning-gemini.md) | `llm/`, `fixtures/contracts/` |
| P4 | Pipeline and UI | [P4-pipeline-ui.md](P4-pipeline-ui.md) | `app.py`, `pipeline.py`, `fixtures/runs/`, `requirements.txt` |
| all | Shared formats | | `models/schemas.py` (change only after telling the team) |

Each person commits only inside their own folders. `tests/`: each person their own files.

## Timeline

| Time | What happens |
|---|---|
| 0:00–0:30 | Everyone: read `models/schemas.py`, agree the hero dataset settings, get a Gemini key into `.env`. Don't let this run long. |
| 0:30–2:00 | Build alone against fixture files. P1 tools, P2 dataset + plain-AI test, P3 Gemini calls, P4 UI on a fake event stream. |
| **2:00** | **Checkpoint: the whole flow works with no LLM.** Hardcoded contracts → real calculations → `judge` → UI. Hero shows Customer X WEAKENED, product SUPPORTED. If you get here, you have a demo no matter what. P4 integrates. |
| 2:00–3:30 | Gemini connected end to end, report added. P2 builds Dataset A and the pitch. |
| 3:30–4:15 | "Your theory" box, UI polish, critic drilldown **only if on schedule**. Save Gemini responses for offline replay. |
| 4:15–5:00 | **Freeze.** Bug fixes only. Rehearse twice with a timer. |

If something slips, cut scope from the next block. Never skip the 2:00 checkpoint.

## Handoffs

| From → To | What | By |
|---|---|---|
| P1 → P3, P4 | Sample Evidence JSON per tool, `TOOL_SPECS` | 0:45 |
| P3 → P4 | `fixtures/contracts/hero.json` | 0:45 |
| P2 → P1, P4 | `data/hero.csv` + `data/answer_key.json` | 1:00 |
| P2 → P3 | Plain-AI result: does plain Gemini blame Customer X? | 1:30 |
| P1 → P4 | `run_tool` and `judge` on real data | 2:00 |
| P3 → P4 | `interpret`, `hypothesize`, `write_contracts`, `report` | 3:00 |

## What `measure` means

The share of the total change a hypothesis accounts for, signed so positive means "same direction as the total change". It can go above 1 or below 0; don't clip it.

Default thresholds: **0.40 or more → SUPPORTED**, **under 0.05 (including negative) → REJECTED**, in between → WEAKENED. Evidence with status `untestable` or `error` → UNTESTABLE. That makes Customer X at 8% WEAKENED and a data-quality gap under 1% REJECTED, matching the hero demo.

## Function signatures

```python
run_tool(df, tool: str, args: dict) -> Evidence                        # P1, analysis/tools.py
judge(contract: Contract, ev: Evidence) -> Label                       # P1, analysis/judge.py
TOOL_SPECS: list[dict]                                                 # P1, analysis/tools.py
run_investigation(csv_path, question, theory=None) -> Iterator[Event]  # P4, pipeline.py
```

## Cut for the 5-hour version

LangGraph (a plain Python generator does the job), price-volume-mix, full seasonality analysis, benchmark scoring, the real UCI dataset, Challenge mode, the waterfall chart and the backup video. Add any of them back only if you're ahead at 3:30.

## Ground rules

- No number on screen comes from the LLM.
- Verdict labels come from `judge()` in code. The LLM writes only the rationale.
- A contract is locked before its test runs and never edited afterwards.
- `main` always runs. Pull often, merge small, and rerun the hero flow after each merge.
- Pandas only.

## On stage

P2 pitches and narrates. P4 drives the laptop (switches to replay if anything fails). P1 answers "Where do the numbers come from?" P3 answers "What does the LLM actually do?"
