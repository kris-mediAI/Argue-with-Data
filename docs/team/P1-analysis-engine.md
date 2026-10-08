# P1 · Analysis engine

> You compute every number the audience sees. Pure pandas, no LLM.

**Owns:** `analysis/`, `tools/`, `fixtures/evidence/`, `tests/test_analysis.py` · **Branch:** `p1-analysis`
**Read first:** [PLAN.md](PLAN.md), `models/schemas.py`, [AGENTS.md](../../AGENTS.md)

## Unblock everyone (by 0:45)

1. `fixtures/evidence/<tool>.json`: one sample Evidence per tool, using the hero story.
2. `TOOL_SPECS` in `tools/registry.py`: each tool's name, description, args, and what its `measure` means. P3 puts this in the Gemma prompt.

## Tools (by 2:00)

Every tool takes `(df, metric, period_a, period_b, **args)` and returns `Evidence`. Periods are `"YYYY-MM"`. `measure = part_change / total_change`, signed. If `total_change == 0`, return `status="error"`.

| Tool (registry key) | File | Tests the hypothesis | measure |
|---|---|---|---|
| `compare_periods` | `analysis/comparisons.py` | (baseline) | None |
| `breakdown` | `analysis/comparisons.py` | region, product | focus member's share, or the top member's |
| `contribution` | `analysis/contributions.py` | customer churn, a specific customer | lost customers' share, or the focus customer's |
| `mix` | `analysis/mix_analysis.py` | product mix shift | mix effect's share (price-volume-mix) |
| `order_volume` | `analysis/comparisons.py` | order volume | share explained by the change in order count |
| `trend` | `analysis/trends.py` | seasonality | untestable without the same months a year earlier |
| `data_quality` | `analysis/data_quality.py` | data problems | artificial change ÷ total change |
| `drilldown` | `analysis/comparisons.py` | critic follow-ups | top-5 members' share of one segment's change |

Also:
- `profile(df)` in `analysis/profiling.py`
- `run_tool(df, tool, args)` in `tools/registry.py`. It validates the tool, args, columns and periods, and **never raises**.
- `verify(contract, evidence)` in `analysis/verify.py`: checks that parts add up and the periods exist, returning a list of problems.
- `judge(contract, evidence)` in `analysis/judge.py`

## After 2:00

Tests in `tests/test_analysis.py`. Then check every number against P2's `data/answer_key.json`.

## On stage

You answer "Where do the numbers come from?"
