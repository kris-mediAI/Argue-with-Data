# P4 · LangGraph and UI

> You build the LangGraph state machine, the Streamlit app and the deployment. You're the integrator at the 2:00 checkpoint.

**Owns:** `graph/`, `ui/`, `app.py`, `requirements.txt`, `tests/test_smoke.py`, the Streamlit Cloud deployment · **Branch:** `p4-graph-ui`
**Read first:** [PLAN.md](PLAN.md) (the graph diagram), `models/schemas.py`, [AGENTS.md](../../AGENTS.md)

## The graph (by 2:00, with stubbed agents)

- **`graph/state.py`:** `InvestigationState` (TypedDict) holding question, dataset_id, profile, intent, baseline, hypotheses, contracts, evidence, verdicts, critic decisions, iteration and report. **Keep the DataFrame out of the state**: store it in a module-level dict keyed by `dataset_id`, so the state stays serializable.
- **`graph/nodes.py`:** one function per node in the PLAN diagram.
  - `lock_contracts` sets `locked_at` and `sha256(json.dumps(contract_without_sha, sort_keys=True))`.
  - `execute_tests` calls P1's `run_tool` for every contract.
  - `verify_results` calls `verify`; `judge` calls `judge`.
  - **Until 3:00, the Gemma nodes return hardcoded values** from `fixtures/contracts/hero.json`.
- **`graph/routing.py`:** `route_next`. Go back to `lock_contracts` if the critic has follow-ups and `iteration < 2`; otherwise go to `final_synthesis`.
- **`graph/graph.py`:** `StateGraph(...)`, `add_conditional_edges("critic", route_next, ...)`, `compile()`.
- A node that returns a list **replaces** that list. Return the full list, or use `Annotated[list, operator.add]`.

## The app

- **Sidebar:** CSV upload or demo dataset picker (demo / churn), plus a profile summary: rows, date range, metrics, dimensions.
- **Main area:**
  - Question box plus an optional **"Your theory"** box.
  - Stage checklist driven by `graph.stream(..., stream_mode="updates")`.
  - Baseline card.
  - **Contract cards** that show the thresholds and "Locked 14:03:07 · sha 3f9a1c", then reveal the result about a second later.
  - Evidence table: Hypothesis | Accounts for | Verdict.
  - Evidence trace expander per hypothesis.
  - Final answer.
- Verdict colors: SUPPORTED green, WEAKENED amber, REJECTED red, UNTESTABLE grey, always shown with the word too. Format ₹ and % in the UI.
- Keep results in `st.session_state`, because Streamlit reruns the whole script on every click.

## Deployment (at 2:00, then again after the freeze)

Streamlit Community Cloud: connect the repo, set `app.py` as the entry point, and put `GEMINI_API_KEY` and `GEMMA_MODEL` in the app's **Secrets**, never in git. Read secrets with `st.secrets` and fall back to `os.environ` locally. Send the live URL to P2.

## On stage

You drive the laptop. If the API fails, switch on `REPLAY=1` and keep going.
