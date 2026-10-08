# P1 · Analysis engine

> You compute every number the audience sees. Pure pandas, no LLM.

**Owns:** `analysis/`, `fixtures/evidence/`, `tests/test_analysis.py`
**Read first:** [PLAN.md](PLAN.md) and `models/schemas.py`

## 0:00–0:45 · Unblock everyone

1. Hand-write `fixtures/evidence/<tool>.json` for each tool below, using the hero story (Customer X about 8%, Premium about 67%). P3 and P4 build against these.
2. Write `TOOL_SPECS` in `analysis/tools.py`: name, one-line description, args, and **what `measure` means** for each tool. P3 pastes this into the Gemini prompt.

## 0:45–2:00 · Build the tools

Every tool: `tool(df, metric, period_a, period_b, **args) -> Evidence`. Periods are `"YYYY-MM"`. `measure = part_change / total_change`, signed, not clipped. If `total_change == 0`, return `status="error"`.

1. **`profile(df) -> dict`** (`analysis/profiler.py`): rows, column types, date column (parse once, add `_month` as `"YYYY-MM"`), metric and dimension candidates, missing %, duplicates, available months.
2. **`compare_periods`**: before, after, abs_change, pct_change. `measure=None` (it's the headline, not a test).
3. **`breakdown(dimension, focus=None)`**: per-member before, after, change, share_of_change, sorted. `measure` = the focus member's share, or the top member's share. Used for product and region.
4. **`customer_bridge(entity="customer", focus=None)`**: lost + new + shrinking + growing customers, **adding up exactly to the total change**. `measure` = lost share, or the focus customer's share (for the user's "it's Customer X" theory).
5. **`data_quality`**: missing values, duplicates, days with no rows per period. `measure` = estimated revenue gap from missing days ÷ total change.
6. **`trend`**: if there are fewer than 13 months of data, return `status="untestable"` with a reason the UI can show: *"Only 3 months of data. Testing seasonality needs the same months from an earlier year."* That's all it needs today.
7. **`run_tool(df, tool, args)`** in `analysis/tools.py`: `TOOL_REGISTRY` lookup, rejects unknown tools, args and columns. **Never raises**; returns `Evidence(status="error", reason=...)`.
8. **`judge`** in `analysis/judge.py`:
   ```python
   def judge(c: Contract, ev: Evidence) -> Label:
       if ev.status != "ok" or ev.measure is None:
           return "UNTESTABLE"
       if ev.measure >= c.support_at_least:
           return "SUPPORTED"
       if ev.measure < c.reject_below:
           return "REJECTED"
       return "WEAKENED"
   ```

**By 2:00:** `run_tool` and `judge` work on `data/hero.csv`, and the numbers match `data/answer_key.json`.

## 2:00–4:15 · Harden and stretch

- `tests/test_analysis.py`: the customer bridge adds up to the total change; each `judge` branch.
- Stretch, only if on schedule at 3:30: **`drilldown(segment_dim, segment_value, inner_dim)`**. It's `breakdown` filtered to one segment (e.g. Premium by customer), with `measure` = the top-5 members' share. The critic uses it to show the premium drop is spread across many customers, so it isn't churn in disguise.

## On stage

You answer "Where do the numbers come from?" Be ready to show one calculation by hand.
