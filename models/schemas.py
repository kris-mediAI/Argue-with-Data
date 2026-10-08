"""Shared data formats. Announce any change in team chat before pushing it."""
from typing import Literal

from pydantic import BaseModel

Label = Literal["SUPPORTED", "WEAKENED", "REJECTED", "UNTESTABLE"]
Status = Literal["PROPOSED", "TESTING", "SUPPORTED", "WEAKENED", "REJECTED", "UNTESTABLE"]


class Intent(BaseModel):
    """parse_question output."""
    metric: str                         # "revenue"
    date_column: str | None = None
    period_a: str                       # "2026-02"
    period_b: str                       # "2026-03"
    dimensions: list[str] = []
    question_type: str = "root_cause"
    user_theory: str | None = None      # "I think it's Customer X"
    assumptions: list[str] = []


class Hypothesis(BaseModel):
    id: str                             # "H1"
    claim: str                          # "Losing Customer X explains the decline"
    source: Literal["user", "system", "critic"]
    required_columns: list[str]
    status: Status = "PROPOSED"         # PROPOSED -> TESTING -> one of the four verdicts


class Contract(BaseModel):
    """A falsification contract. Thresholds are fixed here, before the test runs, and judged in code."""
    hypothesis_id: str
    claim: str
    tool: str                           # key in tools.registry.ANALYSIS_TOOLS
    args: dict                          # includes metric, period_a, period_b; checked by run_tool
    support_at_least: float = 0.40      # measure >= this            -> SUPPORTED
    reject_below: float = 0.05          # measure <  this (or < 0)   -> REJECTED; in between -> WEAKENED
    required_evidence: list[str] = []
    locked_at: str | None = None        # stamped by lock_contracts, before the tool runs
    sha: str | None = None              # sha256 of every other field


class Evidence(BaseModel):
    status: Literal["ok", "untestable", "error"]
    measure: float | None               # signed share of the total change; see docs/team/PLAN.md
    numbers: dict                       # before, after, total_change, ...
    rows: list[dict] = []               # table for the UI
    reason: str | None = None           # why untestable or error


class Verdict(BaseModel):
    hypothesis_id: str
    label: Label                        # from analysis.judge.judge(), never from the LLM
    measure: float | None = None
    rationale: str = ""                 # LLM-written; may only quote numbers found in Evidence


class CriticDecision(BaseModel):
    enough_evidence: bool
    reasoning: str
    alternatives_considered: list[str] = []
    follow_ups: list[Contract] = []     # at most 2 per round


class Report(BaseModel):
    direct_answer: str
    overall_change: str
    strongest_explanation: str
    alternatives: list[str]
    untestable: list[str]
    caveats: list[str]                  # always includes "contribution, not causal proof"
