# P4 · Pipeline and UI

> You wire the pieces together, make the investigation visible, and keep `main` runnable. You're the integrator at the 2:00 checkpoint.

**Owns:** `app.py`, `pipeline.py`, `fixtures/runs/`, `requirements.txt`, `tests/test_smoke.py`
**Read first:** [PLAN.md](PLAN.md) and `models/schemas.py`

## 0:00–2:00 · UI on fake data, then the real pipeline

1. Write `fixtures/runs/hero_fake.json`, a list of Events for a full hero run, built from P1's and P3's fixtures. Write `replay(path, delay=0.6)`, a generator that yields them with pauses, and build the Streamlit page against it.
2. **`pipeline.py`: `run_investigation(csv_path, question, theory=None) -> Iterator[Event]`**. A plain generator, no LangGraph:
   ```
   profile → interpret → headline (compare_periods) → hypothesize → write_contracts
   → for each contract: lock → run_tool → judge → yield events
   → report
   ```
   - **Lock** = set `locked_at` (UTC ISO) and `sha = sha256(json.dumps(contract_without_sha, sort_keys=True))`, yield `contract_locked`, **then** run the tool.
   - **Until P3's functions arrive**, `interpret`, `hypothesize` and `write_contracts` return hardcoded hero values from `fixtures/contracts/hero.json`, and `report` returns a placeholder.
   - Save every run's events to `fixtures/runs/<timestamp>.json`.

**2:00 checkpoint:** the pipeline runs on `data/hero.csv` with real tools and `judge`, and the page shows Customer X WEAKENED and product SUPPORTED.

## The page (`app.py`)

- **Sidebar:** dataset picker (hero, Dataset A, upload) and a **Replay** toggle that plays a saved run with no network.
- **Profile card:** rows, columns, date range, missing data, detected metric and dimensions.
- **Ask:** question box, an optional **"Your theory"** box, an Investigate button.
- **Timeline:** for each hypothesis, show the contract card first: claim, test, "SUPPORTED if ≥ 40% · REJECTED if < 5%", "Locked 14:03:07 · sha 3f9a1c". **Wait about a second, then reveal** the measure and verdict badge. That pause is the drama.
- **Evidence table:** hypothesis, accounts for, verdict, sorted by measure. An expander per hypothesis for the trace: claim → test → rows → result → verdict.
- **Report** at the bottom.
- Verdict colors: SUPPORTED green, WEAKENED amber, REJECTED red, UNTESTABLE grey, always with the word too. Format ₹ and % here, not in the Evidence.

## 2:00–4:15

- Swap in P3's real functions (by 3:00).
- `tests/test_smoke.py`: run the hero with `REPLAY=1` and check the verdicts against `data/answer_key.json`. Run it after every merge.
- Test Replay with Wi-Fi off before 4:15.
- Make switching to Dataset A one click. It's a key demo beat.

## Watch out for

**Streamlit reruns the whole script on every click.** Keep events and results in `st.session_state`, or opening an expander restarts the investigation.

## On stage

You drive the laptop. If anything breaks, switch to Replay and keep going.
