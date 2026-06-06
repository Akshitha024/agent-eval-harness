"""Type definitions for the harness."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Step(BaseModel):
    """One agent step."""

    idx: int
    tool: str
    args_summary: str = ""
    result_summary: str = ""


class Trajectory(BaseModel):
    """One trajectory: id + ordered steps + final answer."""

    tid: str
    steps: list[Step] = Field(default_factory=list)
    final_answer: str = ""


class JudgeVerdict(BaseModel):
    judge_name: str
    score: float = Field(ge=0, le=1)
    rationale: str = ""


class CouncilResult(BaseModel):
    tid: str
    mean_score: float
    verdicts: list[JudgeVerdict]


class DiffReport(BaseModel):
    tid: str
    same_n_steps: bool
    n_step_changes: int
    n_tool_changes: int
    tools_added: list[str] = Field(default_factory=list)
    tools_removed: list[str] = Field(default_factory=list)


class RegressionAlert(BaseModel):
    tid: str
    severity: str
    message: str
