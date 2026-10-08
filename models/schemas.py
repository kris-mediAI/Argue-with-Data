"""Shared data formats. Agreed at 0:00–0:30; announce any change in team chat before pushing it."""
from typing import Literal

from pydantic import BaseModel

Label = Literal["SUPPORTED", "WEAKENED", "REJECTED", "UNTESTABLE"]


class Intent(BaseModel):
    metric: str                         # "revenue"
    period_a: str                       # "2026-02"
    period_b: str                       # "2026-03"
    user_theory: str | None = None      # "I think it's Customer X"
    assumptions: list[str] = []


class Hypothesis(BaseModel):
    id: str                             # "H1"
    claim: str                          # "Losing Customer X explains the decline"
    source: Literal["user", "system", "critic"]
    required_columns: list[str]


class Contract(BaseModel):
    hypothesis_id: str
    claim: str
    tool: str                           # key in analysis.tools.TOOL_REGISTRY
    args: dict                          # checked by run_tool
    support_at_least: float = 0.40      # measure >= this -> SUPPORTED
    reject_below: float = 0.05          # measure <  this -> REJECTED (includes wrong direction)
    locked_at: str | None = None        # stamped before the tool runs
    sha: str | None = None              # sha256 of every other field


class Evidence(BaseModel):
    status: Literal["ok", "untestable", "error"]
    measure: float | None               # signed share of the total change (see docs/team/PLAN.md)
    numbers: dict                       # before, after, abs_change, pct_change, ...
    rows: list[dict] = []               # table for the UI
    reason: str | None = None           # why untestable or error


class Verdict(BaseModel):
    hypothesis_id: str
    label: Label                        # from analysis.judge.judge(), never from the LLM
    rationale: str                      # LLM-written; may only quote numbers found in Evidence


class Report(BaseModel):
    headline: str
    most_supported: str
    alternatives: list[str]
    limitations: list[str]


class Event(BaseModel):
    type: Literal["profiled", "interpreted", "headline", "hypotheses", "contract_locked",
                  "evidence", "verdict", "critic", "report", "error"]
    hypothesis_id: str | None = None
    payload: dict
